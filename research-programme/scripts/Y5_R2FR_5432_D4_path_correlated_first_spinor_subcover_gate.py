from __future__ import annotations

import argparse
import ctypes
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
if os.name == "nt":
    ctypes.windll.kernel32.SetPriorityClass(
        ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
    )


CHECKPOINT = 5432
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
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5431" / "v46_bounded_production_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5431" / "P8_Y5_BRR5396_5431_VALIDATION.csv"
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
DOCUMENT = POST / "5432-Y5-R2FR-D4-path-correlated-first-spinor-subcover-gate.md"
PROBES = OUTPUT / "path_correlated_first_spinor_subcover_rows.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5432_VALIDATION.csv"
RESULT = OUTPUT / "path_correlated_first_spinor_subcover_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v46"
TERM_ID = "MC04_SP_DP"
MAPPED_CELL_ID = "S_X006_MC04_SP_DP"
PATH_SEGMENT = "RIGHT_CONNECTOR"
GLOBAL_ARC_COUNT = 4
EXPECTED_PATHS = {"LLU", "LR", "R"}
BROAD_FLAGS = (
    "valid_for_right_connector_completion",
    "valid_for_regular_away_W3_claim",
    "valid_for_D4_numeric_event_local_W3_bound",
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


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


def arc_displacement(parent: Any, radius: float, arc_index: int) -> Any:
    phase = (
        parent.cbox(arc_index, arc_index + 1)
        * parent.cpoint(2 * math.pi / GLOBAL_ARC_COUNT)
    )
    return parent.cpoint(radius) * (
        parent.iv.cos(phase) + parent.cpoint(1j) * parent.iv.sin(phase)
    )


def finite_spinors(parent: Any, spinors: tuple[list[Any], list[Any]]) -> bool:
    return all(
        math.isfinite(parent.M5258.upper_abs(component))
        for chirality in spinors
        for component in chirality
    )


def probe_box(
    parent: Any,
    cell: dict[str, Any],
    epsilon_row: dict[str, Any],
    box: list[Any],
) -> list[dict[str, Any]]:
    absolute_coordinate = parent.cbox(float(box[0]), float(box[1]))
    path_parameter = parent.cbox(float(box[2]), float(box[3]))
    epsilon = parent.epsilon_interval(epsilon_row)
    energy = parent.deformed_path_energy_dual(
        cell, PATH_SEGMENT, absolute_coordinate, path_parameter
    ).value
    configurations, selector = parent.closed_selector_configuration_subset(
        parent.configuration_variants(TERM_ID),
        absolute_coordinate,
        energy,
        epsilon,
    )
    rows: list[dict[str, Any]] = []
    for configuration in configurations:
        inputs, geometry = parent.interval_inputs(
            configuration, absolute_coordinate, energy, epsilon
        )
        radius = 1.0e-7 * max(
            1.0, parent.M5258.upper_abs(geometry["selected_root"])
        )
        for arc_index in range(GLOBAL_ARC_COUNT):
            displacement = arc_displacement(parent, radius, arc_index)
            direct_status = "PASS"
            try:
                parent.displaced_first_rational_spinors(
                    configuration,
                    inputs,
                    geometry,
                    displacement,
                    1,
                    parent.M5258.IntervalDiagnostics(),
                    "checkpoint_5432_direct_first",
                )
            except parent.M5258.IntervalSingularity:
                direct_status = "FAIL_NO_PIVOT"
            subcover_status = "FAIL"
            chart = ""
            pivot_lower = 0.0
            subdivision_count = 0
            failure = ""
            for candidate_count in (2, 4, 8):
                try:
                    spinors, _, chart, pivot_lower = (
                        parent.subdivided_path_hard_rational_spinors(
                            configuration,
                            cell,
                            PATH_SEGMENT,
                            absolute_coordinate,
                            path_parameter,
                            epsilon,
                            displacement,
                            1,
                            1,
                            parent.M5258.IntervalDiagnostics(),
                            "checkpoint_5432_path_correlated_first",
                            candidate_count,
                        )
                    )
                    if not finite_spinors(parent, spinors):
                        raise ValueError("non-finite spinor enclosure")
                except Exception as error:
                    failure = f"{type(error).__name__}:{error}"[:1000]
                    continue
                subcover_status = "PASS"
                subdivision_count = candidate_count
                failure = ""
                break
            rows.append(
                {
                    "checkpoint": CHECKPOINT,
                    "refinement_path": str(box[5]),
                    "refinement_depth": int(box[4]),
                    "x_lower": float(box[0]),
                    "x_upper": float(box[1]),
                    "t_lower": float(box[2]),
                    "t_upper": float(box[3]),
                    "role": str(configuration["role"]),
                    "arc_index": arc_index,
                    "selector_margin_lower": float(
                        selector["selector_role_margin_lower"]
                    ),
                    "direct_status": direct_status,
                    "subcover_status": subcover_status,
                    "subdivision_count": subdivision_count,
                    "projective_chart": chart,
                    "selected_pivot_abs_lower": float(pivot_lower),
                    "failure": failure,
                    "valid_for_path_correlated_first_spinor_subcover": (
                        subcover_status == "PASS" and pivot_lower > 0.0
                    ),
                    "valid_for_parent_integration": False,
                    **{flag: False for flag in BROAD_FLAGS},
                }
            )
    return rows


def write_document(utility: Any, payload: dict[str, Any]) -> None:
    if payload["valid_for_path_correlated_first_spinor_subcover"]:
        decision = "**PASS FOR A COMMON PATH-CORRELATED PROJECTIVE SUBCOVER ONLY.**"
        interpretation = (
            "One projective family covers every selected chart and contour arc of "
            "the saved frontier."
        )
        next_action = (
            "Integrate the path-correlated hard-leg-1 constructor into a new parent "
            "revision and rerun the production boxes."
        )
    else:
        decision = "**COMMON-FAMILY ROUTE REJECTED; FINITE OUTER CHART COVER RETAINED.**"
        interpretation = (
            "The stronger constructor certifies LLU, but LR and R cross between the "
            "plus and minus projective families. A single spinor gauge cannot cover "
            "those broad boxes, so wiring this fallback into the parent would be an "
            "invalid partial fix. This is a chart transition, not a zero-momentum result."
        )
        next_action = (
            "Use the existing adaptive x/t partition to produce a finite chart cover "
            "of LR and R, then freeze the committed union."
        )
    lines = [
        "# 5432: path-correlated first-spinor subcover gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        interpretation,
        "",
        "## Result",
        "",
        f"- Probe rows: `{payload['probe_row_count']}`.",
        f"- Old direct no-pivot rows: `{payload['direct_failure_count']}`.",
        f"- Path-correlated subcover passes: `{payload['subcover_pass_count']}`.",
        f"- Minimum certified pivot: `{payload['minimum_pivot_abs_lower']:.17g}`.",
        f"- Maximum subdivision count required: `{payload['maximum_subdivision_count']}`.",
        "",
        "## Next integration",
        "",
        next_action,
        "",
        "## Claim boundary",
        "",
        "This is a chart-existence certificate, not right-connector completion and not a W3, UV, local-GR, or full-MTS claim.",
    ]
    utility.atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    utility = load_module("mts_5428_for_5432", UTILITY_SCRIPT)
    parent = load_module("mts_5396_v46_for_5432", PARENT_SCRIPT)
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    previous = utility.read_json(PREVIOUS_RESULT)
    previous_validation = utility.read_csv(PREVIOUS_VALIDATION)
    state = utility.read_json(ACTIVE_STATE)
    input_paths = (
        PARENT_SCRIPT,
        UTILITY_SCRIPT,
        PREVIOUS_RESULT,
        PREVIOUS_VALIDATION,
        ACTIVE_STATE,
        ACTIVE_ROWS,
    )
    hashes_before = {
        str(path.relative_to(POST)): sha256(path) for path in input_paths
    }
    cell, epsilon_row = epsilon_and_cell(parent)
    probe_rows: list[dict[str, Any]] = []
    for box in state["stack"]:
        probe_rows.extend(probe_box(parent, cell, epsilon_row, box))
        utility.atomic_csv(PROBES, probe_rows)
    hashes_after = {
        str(path.relative_to(POST)): sha256(path) for path in input_paths
    }
    passing = [
        row
        for row in probe_rows
        if row["valid_for_path_correlated_first_spinor_subcover"]
    ]
    direct_failures = [
        row for row in probe_rows if row["direct_status"] != "PASS"
    ]
    minimum_pivot = min(
        float(row["selected_pivot_abs_lower"]) for row in passing
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "saved_accepted_box_count": int(state["accepted_count"]),
        "saved_pending_box_count": len(state["stack"]),
        "saved_refinement_paths": [str(box[5]) for box in state["stack"]],
        "probe_row_count": len(probe_rows),
        "direct_failure_count": len(direct_failures),
        "subcover_pass_count": len(passing),
        "minimum_pivot_abs_lower": minimum_pivot,
        "maximum_subdivision_count": max(
            int(row["subdivision_count"]) for row in passing
        ),
        "production_inputs_unchanged": hashes_before == hashes_after,
        "valid_for_path_correlated_first_spinor_subcover": (
            len(passing) == len(probe_rows)
        ),
        "single_family_subcover_rejected": (
            {str(row["refinement_path"]) for row in passing} == {"LLU"}
            and all(
                row["subcover_status"] == "FAIL"
                for row in probe_rows
                if row["refinement_path"] in {"LR", "R"}
            )
        ),
        "valid_for_parent_integration": False,
        **{flag: False for flag in BROAD_FLAGS},
        "provenance_sha256": hashes_before,
    }
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations = [
        utility.check(
            "previous_checkpoint_green",
            int(previous["failed_validation_count"]) == 0
            and all(utility.is_true(row["passed"]) for row in previous_validation),
            f"rows={len(previous_validation)}",
        ),
        utility.check(
            "parent_revision_is_v46",
            parent.REVISION == PARENT_REVISION
            and state["revision"] == PARENT_REVISION,
            f"parent={parent.REVISION}; state={state['revision']}",
        ),
        utility.check(
            "saved_frontier_is_expected",
            int(state["accepted_count"]) == 373
            and len(state["stack"]) == 3
            and {str(box[5]) for box in state["stack"]} == EXPECTED_PATHS,
            f"accepted={state['accepted_count']}; paths={'|'.join(str(box[5]) for box in state['stack'])}",
        ),
        utility.check(
            "legacy_constructor_reproduces_obstruction",
            bool(direct_failures),
            f"direct failures={len(direct_failures)}",
        ),
        utility.check(
            "single_family_result_is_exactly_classified",
            payload["single_family_subcover_rejected"]
            and not payload["valid_for_path_correlated_first_spinor_subcover"],
            f"pass={len(passing)}/{len(probe_rows)}; passing paths={'|'.join(sorted({str(row['refinement_path']) for row in passing}))}",
        ),
        utility.check(
            "all_subcover_pivots_are_positive",
            minimum_pivot > 0.0 and math.isfinite(minimum_pivot),
            f"minimum={minimum_pivot}",
        ),
        utility.check(
            "subcover_is_bounded_by_eight_squared",
            all(int(row["subdivision_count"]) in {2, 4, 8} for row in passing),
            f"maximum={payload['maximum_subdivision_count']}",
        ),
        utility.check(
            "production_inputs_are_hash_immutable",
            hashes_before == hashes_after,
            f"{len(input_paths)} hashes checked",
        ),
        utility.check(
            "parent_integration_not_preclaimed",
            not payload["valid_for_parent_integration"],
            "integration requires v47 and direct production-box tests",
        ),
        utility.check(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_FLAGS),
            "all broad claims false",
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
    write_document(utility, payload)
    utility.atomic_json(RESULT, payload)
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    return payload


def main() -> int:
    payload = run_gate()
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
