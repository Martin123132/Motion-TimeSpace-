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


CHECKPOINT = 5434
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
FORMULA_RESULT = (
    FUNCTIONAL_RG / "5430" / "representative_external41_mirror_disk_result.json"
)
FORMULA_VALIDATION = (
    FUNCTIONAL_RG / "5430" / "P8_Y5_BRR5396_5430_VALIDATION.csv"
)
FRONTIER_PROBES = (
    FUNCTIONAL_RG / "5432" / "path_correlated_first_spinor_subcover_rows.csv"
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
DOCUMENT = POST / "5434-Y5-R2FR-D4-subdivided-representative-ratio-disk-subcover-gate.md"
COVER_ROWS = OUTPUT / "subdivided_representative_ratio_disk_cover_rows.csv"
SUMMARY_ROWS = OUTPUT / "subdivided_representative_ratio_disk_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5434_VALIDATION.csv"
RESULT = OUTPUT / "subdivided_representative_ratio_disk_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v46"
TERM_ID = "MC04_SP_DP"
MAPPED_CELL_ID = "S_X006_MC04_SP_DP"
PATH_SEGMENT = "RIGHT_CONNECTOR"
TARGET_PATHS = {"LR", "R"}
SUBDIVISION_COUNTS = (4, 8, 16, 32)
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


def epsilon_and_cell(parent: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    cell = next(
        row
        for row in parent.away_term_support_cells()
        if row["mapped_cell_id"] == MAPPED_CELL_ID
    )
    arguments = argparse.Namespace(
        combined_regulator_box=True,
        combined_regulator_slab_count=2,
        epsilon_subdivisions=1,
    )
    return cell, parent.epsilon_boxes(arguments)[0]


def targets(utility: Any) -> list[dict[str, Any]]:
    rows = utility.read_csv(FRONTIER_PROBES)
    unique: dict[str, dict[str, Any]] = {}
    for row in rows:
        path = str(row["refinement_path"])
        if path not in TARGET_PATHS:
            continue
        unique[path] = {
            "refinement_path": path,
            "refinement_depth": int(row["refinement_depth"]),
            "x_lower": float(row["x_lower"]),
            "x_upper": float(row["x_upper"]),
            "t_lower": float(row["t_lower"]),
            "t_upper": float(row["t_upper"]),
        }
    return [unique[path] for path in sorted(unique)]


def representative_configuration(
    parent: Any,
    cell: dict[str, Any],
    epsilon: Any,
    target: dict[str, Any],
) -> tuple[dict[str, Any], float]:
    coordinate = parent.cbox(target["x_lower"], target["x_upper"])
    parameter = parent.cbox(target["t_lower"], target["t_upper"])
    energy = parent.deformed_path_energy_dual(
        cell, PATH_SEGMENT, coordinate, parameter
    ).value
    configurations, _ = parent.closed_selector_configuration_subset(
        parent.configuration_variants(TERM_ID), coordinate, energy, epsilon
    )
    configuration = next(
        row for row in configurations if row["role"] == "representative"
    )
    _, geometry = parent.interval_inputs(
        configuration, coordinate, energy, epsilon
    )
    radius = 1.0e-7 * max(
        1.0, parent.M5258.upper_abs(geometry["selected_root"])
    )
    return configuration, radius


def cover_target(
    parent: Any,
    cell: dict[str, Any],
    epsilon: Any,
    target: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    configuration, radius = representative_configuration(
        parent, cell, epsilon, target
    )
    displacement_radius = math.nextafter(radius, math.inf)
    displacement = parent.cbox(
        -displacement_radius,
        displacement_radius,
        -displacement_radius,
        displacement_radius,
    )
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(parent.cpoint(80) + epsilon_squared)
        / (parent.cpoint(64) + epsilon_squared)
        + parent.cpoint(1j)
        * (
            -parent.cpoint(2)
            * epsilon
            / (parent.cpoint(64) + epsilon_squared)
        )
    )
    external_root = -parent.cpoint(1j) * parent.M5394.interval_complex_sqrt(
        -q_value
    )
    selected_rows: list[dict[str, Any]] = []
    selected_summary: dict[str, Any] = {}
    for subdivision_count in SUBDIVISION_COUNTS:
        rows: list[dict[str, Any]] = []
        x_width = target["x_upper"] - target["x_lower"]
        t_width = target["t_upper"] - target["t_lower"]
        for x_index in range(subdivision_count):
            x_lower = (
                target["x_lower"] + x_width * x_index / subdivision_count
            )
            x_upper = (
                target["x_lower"]
                + x_width * (x_index + 1) / subdivision_count
            )
            coordinate = parent.cbox(x_lower, x_upper)
            for t_index in range(subdivision_count):
                t_lower = (
                    target["t_lower"]
                    + t_width * t_index / subdivision_count
                )
                t_upper = (
                    target["t_lower"]
                    + t_width * (t_index + 1) / subdivision_count
                )
                parameter = parent.cbox(t_lower, t_upper)
                ratio = (
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
                normalized = q_value * ratio
                external01_edge = ratio - parent.cpoint(1)
                external41_numerator = parent.cpoint(1) + normalized
                external41_edge = -(
                    external41_numerator
                ) / external_root
                ratio_upper = parent.M5258.upper_abs(ratio)
                normalized_upper = parent.M5258.upper_abs(normalized)
                external01_lower = parent.M5258.lower_abs(external01_edge)
                external41_numerator_lower = parent.M5258.lower_abs(
                    external41_numerator
                )
                external41_lower = parent.M5258.lower_abs(external41_edge)
                external41_reciprocal_upper = math.inf
                if external41_numerator_lower > 0.0:
                    external41_reciprocal_upper = parent.M5258.upper_abs(
                        -external_root / external41_numerator
                    )
                row_passed = (
                    math.isfinite(ratio_upper)
                    and ratio_upper < 1.0
                    and external01_lower > 0.0
                    and external41_numerator_lower > 0.0
                    and math.isfinite(external41_reciprocal_upper)
                )
                rows.append(
                    {
                        "checkpoint": CHECKPOINT,
                        "target_path": target["refinement_path"],
                        "subdivision_count": subdivision_count,
                        "x_index": x_index,
                        "t_index": t_index,
                        "x_lower": x_lower,
                        "x_upper": x_upper,
                        "t_lower": t_lower,
                        "t_upper": t_upper,
                        "ratio_abs_upper": ratio_upper,
                        "normalized_ratio_abs_upper": normalized_upper,
                        "external01_edge_abs_lower": external01_lower,
                        "external41_numerator_abs_lower": (
                            external41_numerator_lower
                        ),
                        "external41_edge_abs_lower": external41_lower,
                        "external41_reciprocal_abs_upper": (
                            external41_reciprocal_upper
                        ),
                        "cell_passed": row_passed,
                        "valid_for_parent_integration": False,
                        "valid_for_right_connector_completion": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
        selected_rows = rows
        selected_summary = {
            "checkpoint": CHECKPOINT,
            **target,
            "subdivision_count": subdivision_count,
            "cover_cell_count": len(rows),
            "maximum_ratio_abs_upper": max(
                float(row["ratio_abs_upper"]) for row in rows
            ),
            "maximum_normalized_ratio_abs_upper": max(
                float(row["normalized_ratio_abs_upper"]) for row in rows
            ),
            "minimum_external01_edge_abs_lower": min(
                float(row["external01_edge_abs_lower"]) for row in rows
            ),
            "minimum_external41_edge_abs_lower": min(
                float(row["external41_edge_abs_lower"]) for row in rows
            ),
            "minimum_external41_numerator_abs_lower": min(
                float(row["external41_numerator_abs_lower"])
                for row in rows
            ),
            "maximum_external41_reciprocal_abs_upper": max(
                float(row["external41_reciprocal_abs_upper"])
                for row in rows
            ),
            "all_cells_passed": all(bool(row["cell_passed"]) for row in rows),
            "valid_for_subdivided_ratio_disk_subcover": all(
                bool(row["cell_passed"]) for row in rows
            ),
            **{flag: False for flag in BROAD_FLAGS},
        }
        if selected_summary["all_cells_passed"]:
            break
    return selected_summary, selected_rows


def write_document(
    utility: Any, payload: dict[str, Any], summaries: list[dict[str, Any]]
) -> None:
    if payload["valid_for_subdivided_ratio_disk_subcover"]:
        decision = "**PASS FOR THE SUBDIVIDED REPRESENTATIVE EDGE SUBCOVER ONLY.**"
        interpretation = (
            "Both broad LR/R boxes admit a finite ratio-disk cover for external01 "
            "and a finite nonzero-numerator cover for external41. The stronger "
            "external41 condition uses `1+qR != 0` directly rather than requiring "
            "the unnecessarily restrictive sufficient condition `|qR|<1`."
        )
    else:
        decision = "**NO UNIFORM EDGE SUBCOVER AT THE TESTED DEPTH.**"
        interpretation = (
            "At least one LR/R cell still misses a strict unit-disk margin. The parent "
            "must remain unchanged and the failed cell becomes the next derivation target."
        )
    lines = [
        "# 5434: subdivided representative ratio-disk subcover gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        interpretation,
        "",
        "## Broad-box summaries",
        "",
    ]
    for row in summaries:
        lines.append(
            f"- `{row['refinement_path']}`: subdivisions `{row['subdivision_count']} x {row['subdivision_count']}`, "
            f"max `|R|={row['maximum_ratio_abs_upper']:.17g}`, max `|qR|={row['maximum_normalized_ratio_abs_upper']:.17g}`, "
            f"min external01 edge `{row['minimum_external01_edge_abs_lower']:.17g}`, "
            f"min `|1+qR|={row['minimum_external41_numerator_abs_lower']:.17g}`, "
            f"max external41 reciprocal `{row['maximum_external41_reciprocal_abs_upper']:.17g}`; pass `{row['all_cells_passed']}`."
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "No parent code is changed here. Right-connector, W3, UV, local-GR, and full-MTS claims remain false.",
        ]
    )
    utility.atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    utility = load_module("mts_5428_for_5434", UTILITY_SCRIPT)
    parent = load_module("mts_5396_v46_for_5434", PARENT_SCRIPT)
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    formula_result = utility.read_json(FORMULA_RESULT)
    formula_validation = utility.read_csv(FORMULA_VALIDATION)
    state_before = ACTIVE_STATE.read_bytes()
    rows_before = ACTIVE_ROWS.read_bytes()
    cell, epsilon_row = epsilon_and_cell(parent)
    epsilon = parent.epsilon_interval(epsilon_row)
    target_rows = targets(utility)
    summaries: list[dict[str, Any]] = []
    cover_rows: list[dict[str, Any]] = []
    for target in target_rows:
        summary, rows = cover_target(parent, cell, epsilon, target)
        summaries.append(summary)
        cover_rows.extend(rows)
        utility.atomic_csv(COVER_ROWS, cover_rows)
        utility.atomic_csv(SUMMARY_ROWS, summaries)
    all_passed = all(
        bool(row["valid_for_subdivided_ratio_disk_subcover"])
        for row in summaries
    )
    failed_cells = [row for row in cover_rows if not bool(row["cell_passed"])]
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "target_count": len(summaries),
        "cover_cell_count": len(cover_rows),
        "maximum_subdivision_count": max(
            int(row["subdivision_count"]) for row in summaries
        ),
        "maximum_ratio_abs_upper": max(
            float(row["maximum_ratio_abs_upper"]) for row in summaries
        ),
        "maximum_normalized_ratio_abs_upper": max(
            float(row["maximum_normalized_ratio_abs_upper"])
            for row in summaries
        ),
        "minimum_external01_edge_abs_lower": min(
            float(row["minimum_external01_edge_abs_lower"])
            for row in summaries
        ),
        "minimum_external41_edge_abs_lower": min(
            float(row["minimum_external41_edge_abs_lower"])
            for row in summaries
        ),
        "minimum_external41_numerator_abs_lower": min(
            float(row["minimum_external41_numerator_abs_lower"])
            for row in summaries
        ),
        "maximum_external41_reciprocal_abs_upper": max(
            float(row["maximum_external41_reciprocal_abs_upper"])
            for row in summaries
        ),
        "valid_for_subdivided_ratio_disk_subcover": all_passed,
        "failed_cover_cell_count": len(failed_cells),
        "isotropic_cover_rejected": (
            not all_passed
            and len(failed_cells) == 64
            and all(float(row["t_lower"]) == 0.0 for row in failed_cells)
            and all(float(row["t_upper"]) == 1.0 / 32.0 for row in failed_cells)
            and all(float(row["ratio_abs_upper"]) < 1.0 for row in failed_cells)
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
        utility.check(
            "checkpoint_5430_formula_is_green",
            int(formula_result["failed_validation_count"]) == 0
            and all(utility.is_true(row["passed"]) for row in formula_validation),
            f"rows={len(formula_validation)}",
        ),
        utility.check(
            "parent_revision_is_v46",
            parent.REVISION == PARENT_REVISION,
            parent.REVISION,
        ),
        utility.check(
            "targets_are_exactly_lr_and_r",
            {row["refinement_path"] for row in summaries} == TARGET_PATHS,
            "|".join(row["refinement_path"] for row in summaries),
        ),
        utility.check(
            "isotropic_result_is_exactly_classified",
            payload["isotropic_cover_rejected"] and len(summaries) == 2,
            f"failed cells={len(failed_cells)}",
        ),
        utility.check(
            "external01_unit_disk_margin_is_strict",
            payload["maximum_ratio_abs_upper"] < 1.0,
            f"maximum={payload['maximum_ratio_abs_upper']}",
        ),
        utility.check(
            "external41_mirror_disk_is_correctly_not_assumed",
            payload["maximum_normalized_ratio_abs_upper"] >= 1.0,
            f"maximum={payload['maximum_normalized_ratio_abs_upper']}",
        ),
        utility.check(
            "external01_passes_while_external41_boundary_strip_remains",
            payload["minimum_external01_edge_abs_lower"] > 0.0
            and payload["minimum_external41_numerator_abs_lower"] == 0.0,
            f"external01={payload['minimum_external01_edge_abs_lower']}; external41 numerator={payload['minimum_external41_numerator_abs_lower']}",
        ),
        utility.check(
            "external41_reciprocal_is_not_preclaimed",
            not math.isfinite(payload["maximum_external41_reciprocal_abs_upper"])
            and not payload["valid_for_parent_integration"],
            f"maximum={payload['maximum_external41_reciprocal_abs_upper']}",
        ),
        utility.check(
            "production_state_is_hash_immutable",
            state_unchanged,
            "state and accepted-row bytes unchanged",
        ),
        utility.check(
            "parent_integration_not_preclaimed",
            not payload["valid_for_parent_integration"],
            "v47 integration and direct box tests remain required",
        ),
        utility.check(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_FLAGS),
            "all broad flags false",
        ),
        utility.check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"files modified after start={len(formalization_touches)}",
        ),
    ]
    utility.atomic_csv(VALIDATION, validations)
    payload["validation_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    write_document(utility, payload, summaries)
    utility.atomic_json(RESULT, payload)
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    return payload


def main() -> int:
    payload = run_gate()
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
