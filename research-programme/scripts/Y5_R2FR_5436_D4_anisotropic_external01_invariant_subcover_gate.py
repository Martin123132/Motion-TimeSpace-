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


CHECKPOINT = 5436
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
ANISOTROPIC_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5435_D4_anisotropic_representative_mirror_disk_cover_gate.py"
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5435" / "anisotropic_representative_mirror_disk_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5435" / "P8_Y5_BRR5396_5435_VALIDATION.csv"
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
DOCUMENT = POST / "5436-Y5-R2FR-D4-anisotropic-external01-invariant-subcover-gate.md"
COVER_ROWS = OUTPUT / "anisotropic_external01_invariant_cover_rows.csv"
SUMMARY_ROWS = OUTPUT / "anisotropic_external01_invariant_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5436_VALIDATION.csv"
RESULT = OUTPUT / "anisotropic_external01_invariant_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v47"
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
    x_width = target["x_upper"] - target["x_lower"]
    t_width = target["t_upper"] - target["t_lower"]
    x_count = int(math.ceil(x_width / X_TARGET_WIDTH))
    rows: list[dict[str, Any]] = []
    enclosures: list[Any] = []
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
            invariant = parent.centered_path_correlated_external_first_invariant(
                configuration,
                cell,
                PATH_SEGMENT,
                coordinate,
                parameter,
                epsilon,
                displacement,
                0,
            )
            invariant_lower = parent.M5258.lower_abs(invariant)
            real_lower, real_upper = parent.M5394.real_bounds(invariant)
            imaginary_lower, imaginary_upper = (
                parent.M5394.imaginary_bounds(invariant)
            )
            enclosures.append(invariant)
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
                    "invariant_real_lower": real_lower,
                    "invariant_real_upper": real_upper,
                    "invariant_imaginary_lower": imaginary_lower,
                    "invariant_imaginary_upper": imaginary_upper,
                    "invariant_abs_lower": invariant_lower,
                    "cell_passed": invariant_lower > 0.0,
                    **{flag: False for flag in BROAD_FLAGS},
                }
            )
        if x_index % 8 == 0 or x_index + 1 == x_count:
            print(
                json.dumps(
                    {
                        "state": "invariant_cover_progress",
                        "target": target["refinement_path"],
                        "completed_x_slabs": x_index + 1,
                        "total_x_slabs": x_count,
                    }
                ),
                flush=True,
            )
    hull = parent.rectangular_interval_hull(enclosures)
    hull_real_lower, hull_real_upper = parent.M5394.real_bounds(hull)
    hull_imaginary_lower, hull_imaginary_upper = (
        parent.M5394.imaginary_bounds(hull)
    )
    summary = {
        "checkpoint": CHECKPOINT,
        **target,
        "x_subdivision_count": x_count,
        "t_subdivision_count": T_SUBDIVISION_COUNT,
        "cover_cell_count": len(rows),
        "minimum_cell_invariant_abs_lower": min(
            float(row["invariant_abs_lower"]) for row in rows
        ),
        "hull_real_lower": hull_real_lower,
        "hull_real_upper": hull_real_upper,
        "hull_imaginary_lower": hull_imaginary_lower,
        "hull_imaginary_upper": hull_imaginary_upper,
        "hull_invariant_abs_lower": parent.M5258.lower_abs(hull),
        "failed_cell_count": sum(not bool(row["cell_passed"]) for row in rows),
        "valid_for_anisotropic_external01_invariant_subcover": (
            all(bool(row["cell_passed"]) for row in rows)
            and parent.M5258.lower_abs(hull) > 0.0
        ),
        **{flag: False for flag in BROAD_FLAGS},
    }
    return summary, rows


def write_document(
    utility: Any, payload: dict[str, Any], summaries: list[dict[str, Any]]
) -> None:
    if payload["valid_for_anisotropic_external01_invariant_subcover"]:
        decision = "**PASS FOR THE EXTERNAL01 INVARIANT SUBCOVER ONLY.**"
        interpretation = (
            "The same anisotropic LR/R cover keeps `s01` in a common nonzero "
            "rectangular enclosure. Together with the v47 square-edge disk cover, "
            "the exact identity `1/<01> = [01]/s01` supplies the newly exposed "
            "chirality-0 reciprocal without an independent edge closure."
        )
    else:
        decision = "**EXTERNAL01 INVARIANT SUBCOVER REMAINS OPEN.**"
        interpretation = (
            "At least one cell or the common hull reaches zero; v47 remains unchanged."
        )
    lines = [
        "# 5436: anisotropic external01 invariant subcover gate",
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
            f"minimum cell `|s01|={row['minimum_cell_invariant_abs_lower']:.17g}`, "
            f"common-hull `|s01|={row['hull_invariant_abs_lower']:.17g}`, "
            f"failed cells `{row['failed_cell_count']}`."
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "No parent integration is claimed here. Right-connector, W3, UV, local-GR, and full-MTS claims remain false.",
        ]
    )
    utility.atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    utility = load_module("mts_5428_for_5436", UTILITY_SCRIPT)
    isotropic = load_module("mts_5434_for_5436", ISOTROPIC_SCRIPT)
    parent = load_module("mts_5396_v47_for_5436", PARENT_SCRIPT)
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
        summary, rows = cover_target(parent, isotropic, cell, epsilon, target)
        summaries.append(summary)
        all_rows.extend(rows)
        utility.atomic_csv(COVER_ROWS, all_rows)
        utility.atomic_csv(SUMMARY_ROWS, summaries)
    all_passed = all(
        bool(row["valid_for_anisotropic_external01_invariant_subcover"])
        for row in summaries
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "target_count": len(summaries),
        "cover_cell_count": len(all_rows),
        "minimum_cell_invariant_abs_lower": min(
            float(row["minimum_cell_invariant_abs_lower"])
            for row in summaries
        ),
        "minimum_hull_invariant_abs_lower": min(
            float(row["hull_invariant_abs_lower"]) for row in summaries
        ),
        "failed_cell_count": sum(
            int(row["failed_cell_count"]) for row in summaries
        ),
        "valid_for_anisotropic_external01_invariant_subcover": all_passed,
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
            "checkpoint_5435_green",
            int(previous["failed_validation_count"]) == 0
            and bool(previous["valid_for_anisotropic_mirror_disk_cover"])
            and all(utility.is_true(row["passed"]) for row in previous_validation),
            f"rows={len(previous_validation)}",
        ),
        utility.check(
            "parent_revision_is_v47",
            parent.REVISION == PARENT_REVISION,
            parent.REVISION,
        ),
        utility.check(
            "both_targets_have_nonzero_invariant_subcover",
            all_passed and len(summaries) == 2,
            f"failed cells={payload['failed_cell_count']}",
        ),
        utility.check(
            "all_cell_invariants_are_nonzero",
            payload["minimum_cell_invariant_abs_lower"] > 0.0,
            f"minimum={payload['minimum_cell_invariant_abs_lower']}",
        ),
        utility.check(
            "common_hulls_are_nonzero",
            payload["minimum_hull_invariant_abs_lower"] > 0.0,
            f"minimum={payload['minimum_hull_invariant_abs_lower']}",
        ),
        utility.check(
            "production_state_is_hash_immutable",
            state_unchanged,
            "state and accepted-row bytes unchanged",
        ),
        utility.check(
            "parent_integration_not_preclaimed",
            not payload["valid_for_parent_integration"],
            "v48 integration remains required",
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
