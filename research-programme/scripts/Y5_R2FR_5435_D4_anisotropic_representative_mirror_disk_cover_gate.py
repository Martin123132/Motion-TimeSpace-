from __future__ import annotations

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


CHECKPOINT = 5435
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
    FUNCTIONAL_RG / "5434" / "subdivided_representative_ratio_disk_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5434" / "P8_Y5_BRR5396_5434_VALIDATION.csv"
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
DOCUMENT = POST / "5435-Y5-R2FR-D4-anisotropic-representative-mirror-disk-cover-gate.md"
COVER_ROWS = OUTPUT / "anisotropic_representative_mirror_disk_cover_rows.csv"
SUMMARY_ROWS = OUTPUT / "anisotropic_representative_mirror_disk_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5435_VALIDATION.csv"
RESULT = OUTPUT / "anisotropic_representative_mirror_disk_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v46"
PATH_SEGMENT = "RIGHT_CONNECTOR"
X_TARGET_WIDTH = 1.54e-4
T_SUBDIVISION_COUNT = 128
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


def cover_target(
    parent: Any,
    isotropic: Any,
    cell: dict[str, Any],
    epsilon: Any,
    target: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    configuration, radius = isotropic.representative_configuration(
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
    external_root_upper = parent.M5258.upper_abs(external_root)
    x_width = target["x_upper"] - target["x_lower"]
    t_width = target["t_upper"] - target["t_lower"]
    x_count = int(math.ceil(x_width / X_TARGET_WIDTH))
    rows: list[dict[str, Any]] = []
    for x_index in range(x_count):
        x_lower = target["x_lower"] + x_width * x_index / x_count
        x_upper = target["x_lower"] + x_width * (x_index + 1) / x_count
        coordinate = parent.cbox(x_lower, x_upper)
        for t_index in range(T_SUBDIVISION_COUNT):
            t_lower = (
                target["t_lower"]
                + t_width * t_index / T_SUBDIVISION_COUNT
            )
            t_upper = (
                target["t_lower"]
                + t_width * (t_index + 1) / T_SUBDIVISION_COUNT
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
            ratio_upper = parent.M5258.upper_abs(ratio)
            normalized_upper = parent.M5258.upper_abs(normalized)
            external01_lower = 1.0 - ratio_upper
            external41_lower = (
                (1.0 - normalized_upper) / external_root_upper
            )
            external01_reciprocal_upper = (
                math.inf
                if external01_lower <= 0.0
                else 1.0 / external01_lower
            )
            external41_reciprocal_upper = (
                math.inf
                if external41_lower <= 0.0
                else external_root_upper / (1.0 - normalized_upper)
            )
            cell_passed = (
                math.isfinite(ratio_upper)
                and ratio_upper < 1.0
                and math.isfinite(normalized_upper)
                and normalized_upper < 1.0
                and external01_lower > 0.0
                and external41_lower > 0.0
            )
            rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "target_path": target["refinement_path"],
                    "x_subdivision_count": x_count,
                    "t_subdivision_count": T_SUBDIVISION_COUNT,
                    "x_index": x_index,
                    "t_index": t_index,
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "t_lower": t_lower,
                    "t_upper": t_upper,
                    "ratio_abs_upper": ratio_upper,
                    "normalized_ratio_abs_upper": normalized_upper,
                    "external01_disk_edge_abs_lower": external01_lower,
                    "external41_mirror_edge_abs_lower": external41_lower,
                    "external01_reciprocal_abs_upper": (
                        external01_reciprocal_upper
                    ),
                    "external41_reciprocal_abs_upper": (
                        external41_reciprocal_upper
                    ),
                    "cell_passed": cell_passed,
                    **{flag: False for flag in BROAD_FLAGS},
                }
            )
        if x_index % 8 == 0 or x_index + 1 == x_count:
            print(
                json.dumps(
                    {
                        "state": "anisotropic_cover_progress",
                        "target": target["refinement_path"],
                        "completed_x_slabs": x_index + 1,
                        "total_x_slabs": x_count,
                    }
                ),
                flush=True,
            )
    summary = {
        "checkpoint": CHECKPOINT,
        **target,
        "x_subdivision_count": x_count,
        "t_subdivision_count": T_SUBDIVISION_COUNT,
        "cover_cell_count": len(rows),
        "maximum_ratio_abs_upper": max(
            float(row["ratio_abs_upper"]) for row in rows
        ),
        "maximum_normalized_ratio_abs_upper": max(
            float(row["normalized_ratio_abs_upper"]) for row in rows
        ),
        "minimum_external01_disk_edge_abs_lower": min(
            float(row["external01_disk_edge_abs_lower"]) for row in rows
        ),
        "minimum_external41_mirror_edge_abs_lower": min(
            float(row["external41_mirror_edge_abs_lower"]) for row in rows
        ),
        "maximum_external01_reciprocal_abs_upper": max(
            float(row["external01_reciprocal_abs_upper"]) for row in rows
        ),
        "maximum_external41_reciprocal_abs_upper": max(
            float(row["external41_reciprocal_abs_upper"]) for row in rows
        ),
        "failed_cell_count": sum(not bool(row["cell_passed"]) for row in rows),
        "valid_for_anisotropic_mirror_disk_cover": all(
            bool(row["cell_passed"]) for row in rows
        ),
        **{flag: False for flag in BROAD_FLAGS},
    }
    return summary, rows


def write_document(
    utility: Any, payload: dict[str, Any], summaries: list[dict[str, Any]]
) -> None:
    if payload["valid_for_anisotropic_mirror_disk_cover"]:
        decision = "**PASS FOR THE ANISOTROPIC REPRESENTATIVE EDGE COVER ONLY.**"
        interpretation = (
            "The 5434 failure was caused by using equal x/t subdivisions. Resolving "
            "the thin t=0 boundary layer at the scale already demonstrated by the "
            "accepted production boxes gives strict external01 and external41 disk margins "
            "over both original broad LR/R boxes."
        )
    else:
        decision = "**ANISOTROPIC COVER REMAINS OPEN.**"
        interpretation = (
            "At least one cell still lacks a strict disk margin; no parent integration is authorized."
        )
    lines = [
        "# 5435: anisotropic representative mirror-disk cover gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        interpretation,
        "",
        "## Cover summaries",
        "",
    ]
    for row in summaries:
        lines.append(
            f"- `{row['refinement_path']}`: `{row['x_subdivision_count']} x {row['t_subdivision_count']}` cells; "
            f"max `|R|={row['maximum_ratio_abs_upper']:.17g}`, max `|qR|={row['maximum_normalized_ratio_abs_upper']:.17g}`, "
            f"external01 floor `{row['minimum_external01_disk_edge_abs_lower']:.17g}`, "
            f"external41 floor `{row['minimum_external41_mirror_edge_abs_lower']:.17g}`, "
            f"failed cells `{row['failed_cell_count']}`."
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This cover is not yet integrated into the parent. Right-connector, W3, UV, local-GR, and full-MTS claims remain false.",
        ]
    )
    utility.atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    utility = load_module("mts_5428_for_5435", UTILITY_SCRIPT)
    isotropic = load_module("mts_5434_for_5435", ISOTROPIC_SCRIPT)
    parent = load_module("mts_5396_v46_for_5435", PARENT_SCRIPT)
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    previous = utility.read_json(PREVIOUS_RESULT)
    previous_validation = utility.read_csv(PREVIOUS_VALIDATION)
    state_before = ACTIVE_STATE.read_bytes()
    rows_before = ACTIVE_ROWS.read_bytes()
    cell, epsilon_row = isotropic.epsilon_and_cell(parent)
    epsilon = parent.epsilon_interval(epsilon_row)
    target_rows = isotropic.targets(utility)
    summaries: list[dict[str, Any]] = []
    all_rows: list[dict[str, Any]] = []
    for target in target_rows:
        summary, rows = cover_target(
            parent, isotropic, cell, epsilon, target
        )
        summaries.append(summary)
        all_rows.extend(rows)
        utility.atomic_csv(COVER_ROWS, all_rows)
        utility.atomic_csv(SUMMARY_ROWS, summaries)
    all_passed = all(
        bool(row["valid_for_anisotropic_mirror_disk_cover"])
        for row in summaries
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "target_count": len(summaries),
        "cover_cell_count": len(all_rows),
        "maximum_ratio_abs_upper": max(
            float(row["maximum_ratio_abs_upper"]) for row in summaries
        ),
        "maximum_normalized_ratio_abs_upper": max(
            float(row["maximum_normalized_ratio_abs_upper"])
            for row in summaries
        ),
        "minimum_external01_disk_edge_abs_lower": min(
            float(row["minimum_external01_disk_edge_abs_lower"])
            for row in summaries
        ),
        "minimum_external41_mirror_edge_abs_lower": min(
            float(row["minimum_external41_mirror_edge_abs_lower"])
            for row in summaries
        ),
        "maximum_external01_reciprocal_abs_upper": max(
            float(row["maximum_external01_reciprocal_abs_upper"])
            for row in summaries
        ),
        "maximum_external41_reciprocal_abs_upper": max(
            float(row["maximum_external41_reciprocal_abs_upper"])
            for row in summaries
        ),
        "failed_cell_count": sum(
            int(row["failed_cell_count"]) for row in summaries
        ),
        "valid_for_anisotropic_mirror_disk_cover": all_passed,
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
            "checkpoint_5434_green_and_isotropic_cover_rejected",
            int(previous["failed_validation_count"]) == 0
            and bool(previous["isotropic_cover_rejected"])
            and all(utility.is_true(row["passed"]) for row in previous_validation),
            f"rows={len(previous_validation)}",
        ),
        utility.check(
            "parent_revision_is_v46",
            parent.REVISION == PARENT_REVISION,
            parent.REVISION,
        ),
        utility.check(
            "both_targets_have_complete_anisotropic_cover",
            all_passed and len(summaries) == 2,
            f"failed cells={payload['failed_cell_count']}",
        ),
        utility.check(
            "external01_disk_margin_is_strict",
            payload["maximum_ratio_abs_upper"] < 1.0
            and payload["minimum_external01_disk_edge_abs_lower"] > 0.0,
            f"maximum={payload['maximum_ratio_abs_upper']}; floor={payload['minimum_external01_disk_edge_abs_lower']}",
        ),
        utility.check(
            "external41_mirror_disk_margin_is_strict",
            payload["maximum_normalized_ratio_abs_upper"] < 1.0
            and payload["minimum_external41_mirror_edge_abs_lower"] > 0.0,
            f"maximum={payload['maximum_normalized_ratio_abs_upper']}; floor={payload['minimum_external41_mirror_edge_abs_lower']}",
        ),
        utility.check(
            "reciprocal_bounds_are_finite",
            math.isfinite(payload["maximum_external01_reciprocal_abs_upper"])
            and math.isfinite(payload["maximum_external41_reciprocal_abs_upper"]),
            f"external01={payload['maximum_external01_reciprocal_abs_upper']}; external41={payload['maximum_external41_reciprocal_abs_upper']}",
        ),
        utility.check(
            "production_state_is_hash_immutable",
            state_unchanged,
            "state and accepted-row bytes unchanged",
        ),
        utility.check(
            "parent_integration_not_preclaimed",
            not payload["valid_for_parent_integration"],
            "v47 integration remains required",
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
