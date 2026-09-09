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


CHECKPOINT = 5438
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
RATIO_SUMMARY = (
    FUNCTIONAL_RG / "5435" / "anisotropic_representative_mirror_disk_summary.csv"
)
RATIO_RESULT = (
    FUNCTIONAL_RG / "5435" / "anisotropic_representative_mirror_disk_result.json"
)
PREVIOUS_ROWS = (
    FUNCTIONAL_RG / "5436" / "anisotropic_external01_invariant_cover_rows.csv"
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5436" / "anisotropic_external01_invariant_result.json"
)
POINTWISE_RESULT = (
    FUNCTIONAL_RG / "5437" / "external01_endpoint_zero_and_pole_order_result.json"
)
POINTWISE_VALIDATION = (
    FUNCTIONAL_RG / "5437" / "P8_Y5_BRR5396_5437_VALIDATION.csv"
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
DOCUMENT = (
    POST
    / "5438-Y5-R2FR-D4-anisotropic-endpoint-t-negative-real-invariant-subcover-gate.md"
)
COVER_ROWS = OUTPUT / "external01_negative_real_invariant_cover_rows.csv"
SUMMARY_ROWS = OUTPUT / "external01_negative_real_invariant_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5438_VALIDATION.csv"
RESULT = OUTPUT / "external01_negative_real_invariant_subcover_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v47"
PATH_SEGMENT = "RIGHT_CONNECTOR"
COARSE_T_SUBDIVISION_COUNT = 128
ENDPOINT_COARSE_T_COUNT = 9
MAXIMUM_T_REFINEMENT_DEPTH = 4
TARGET_X_SUBDIVISION_COUNTS = {"LR": 8, "R": 32}
EXPECTED_PREVIOUS_CELL_COUNT = 24576
EXPECTED_PREVIOUS_FAILED_COUNT = 1344
EXPECTED_NONNEGATIVE_REAL_COUNT = 1728
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


def invariant_bounds(parent: Any, value: Any) -> dict[str, float]:
    real_lower, real_upper = parent.M5394.real_bounds(value)
    imaginary_lower, imaginary_upper = parent.M5394.imaginary_bounds(value)
    return {
        "invariant_real_lower": real_lower,
        "invariant_real_upper": real_upper,
        "invariant_imaginary_lower": imaginary_lower,
        "invariant_imaginary_upper": imaginary_upper,
        "invariant_abs_lower": parent.M5258.lower_abs(value),
        "invariant_abs_upper": parent.M5258.upper_abs(value),
    }


def stored_bounds(row: dict[str, str]) -> dict[str, float]:
    return {
        "invariant_real_lower": float(row["invariant_real_lower"]),
        "invariant_real_upper": float(row["invariant_real_upper"]),
        "invariant_imaginary_lower": float(
            row["invariant_imaginary_lower"]
        ),
        "invariant_imaginary_upper": float(
            row["invariant_imaginary_upper"]
        ),
        "invariant_abs_lower": float(row["invariant_abs_lower"]),
        "invariant_abs_upper": math.hypot(
            max(
                abs(float(row["invariant_real_lower"])),
                abs(float(row["invariant_real_upper"])),
            ),
            max(
                abs(float(row["invariant_imaginary_lower"])),
                abs(float(row["invariant_imaginary_upper"])),
            ),
        ),
    }


def hull_bounds(rows: list[dict[str, Any]]) -> dict[str, float]:
    real_lower = min(float(row["invariant_real_lower"]) for row in rows)
    real_upper = max(float(row["invariant_real_upper"]) for row in rows)
    imaginary_lower = min(
        float(row["invariant_imaginary_lower"]) for row in rows
    )
    imaginary_upper = max(
        float(row["invariant_imaginary_upper"]) for row in rows
    )
    abs_lower = -real_upper if real_upper < 0.0 else 0.0
    abs_upper = math.hypot(
        max(abs(real_lower), abs(real_upper)),
        max(abs(imaginary_lower), abs(imaginary_upper)),
    )
    return {
        "invariant_real_lower": real_lower,
        "invariant_real_upper": real_upper,
        "invariant_imaginary_lower": imaginary_lower,
        "invariant_imaginary_upper": imaginary_upper,
        "invariant_abs_lower": abs_lower,
        "invariant_abs_upper": abs_upper,
    }


def evaluated_invariant(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
    displacement: Any,
) -> Any:
    return parent.centered_path_correlated_external_first_invariant(
        configuration,
        cell,
        PATH_SEGMENT,
        coordinate,
        parameter,
        epsilon,
        displacement,
        0,
    )


def evaluated_leaf(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    epsilon: Any,
    displacement: Any,
    target_path: str,
    x_index: int,
    coarse_t_index: int,
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
    depth: int,
    refinement_path: str,
) -> dict[str, Any]:
    invariant = evaluated_invariant(
        parent,
        configuration,
        cell,
        parent.cbox(x_lower, x_upper),
        parent.cbox(t_lower, t_upper),
        epsilon,
        displacement,
    )
    bounds = invariant_bounds(parent, invariant)
    return {
        "checkpoint": CHECKPOINT,
        "target_path": target_path,
        "cover_method": "ADAPTIVE_ENDPOINT_T_NEGATIVE_REAL",
        "x_index": x_index,
        "coarse_t_index": coarse_t_index,
        "t_refinement_depth": depth,
        "t_refinement_path": refinement_path,
        "x_lower": x_lower,
        "x_upper": x_upper,
        "t_lower": t_lower,
        "t_upper": t_upper,
        **bounds,
        "negative_real_certified": bounds["invariant_real_upper"] < 0.0,
        "cell_passed": bounds["invariant_real_upper"] < 0.0,
        **{flag: False for flag in BROAD_FLAGS},
    }


def refine_t_cell(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    epsilon: Any,
    displacement: Any,
    target_path: str,
    x_index: int,
    coarse_t_index: int,
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
    depth: int,
    refinement_path: str,
) -> tuple[list[dict[str, Any]], int]:
    row = evaluated_leaf(
        parent,
        configuration,
        cell,
        epsilon,
        displacement,
        target_path,
        x_index,
        coarse_t_index,
        x_lower,
        x_upper,
        t_lower,
        t_upper,
        depth,
        refinement_path,
    )
    if bool(row["cell_passed"]) or depth >= MAXIMUM_T_REFINEMENT_DEPTH:
        return [row], 1
    midpoint = (t_lower + t_upper) / 2.0
    left_rows, left_evaluations = refine_t_cell(
        parent,
        configuration,
        cell,
        epsilon,
        displacement,
        target_path,
        x_index,
        coarse_t_index,
        x_lower,
        x_upper,
        t_lower,
        midpoint,
        depth + 1,
        refinement_path + "L",
    )
    right_rows, right_evaluations = refine_t_cell(
        parent,
        configuration,
        cell,
        epsilon,
        displacement,
        target_path,
        x_index,
        coarse_t_index,
        x_lower,
        x_upper,
        midpoint,
        t_upper,
        depth + 1,
        refinement_path + "R",
    )
    return left_rows + right_rows, 1 + left_evaluations + right_evaluations


def retained_tail_rows(
    target_path: str, source_rows: list[dict[str, str]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for t_index in range(
        ENDPOINT_COARSE_T_COUNT, COARSE_T_SUBDIVISION_COUNT
    ):
        source_group = [
            row for row in source_rows if int(row["t_index"]) == t_index
        ]
        bounds = hull_bounds([stored_bounds(row) for row in source_group])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "target_path": target_path,
                "cover_method": "5436_NEGATIVE_REAL_TAIL_HULL",
                "x_index": -1,
                "coarse_t_index": t_index,
                "t_refinement_depth": 0,
                "t_refinement_path": "TAIL",
                "x_lower": min(float(row["x_lower"]) for row in source_group),
                "x_upper": max(float(row["x_upper"]) for row in source_group),
                "t_lower": min(float(row["t_lower"]) for row in source_group),
                "t_upper": max(float(row["t_upper"]) for row in source_group),
                **bounds,
                "negative_real_certified": bounds["invariant_real_upper"] < 0.0,
                "cell_passed": bounds["invariant_real_upper"] < 0.0,
                **{flag: False for flag in BROAD_FLAGS},
            }
        )
    return rows


def cover_target(
    parent: Any,
    isotropic: Any,
    cell: dict[str, Any],
    epsilon: Any,
    target: dict[str, Any],
    source_rows: list[dict[str, str]],
    ratio_row: dict[str, str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    target_path = str(target["refinement_path"])
    x_count = TARGET_X_SUBDIVISION_COUNTS[target_path]
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
    rows = retained_tail_rows(target_path, source_rows)
    evaluation_count = 0
    x_width = (float(target["x_upper"]) - float(target["x_lower"])) / x_count
    t_width = (float(target["t_upper"]) - float(target["t_lower"])) / 128.0
    for x_index in range(x_count):
        x_lower = float(target["x_lower"]) + x_width * x_index
        x_upper = float(target["x_lower"]) + x_width * (x_index + 1)
        for coarse_t_index in range(ENDPOINT_COARSE_T_COUNT):
            t_lower = float(target["t_lower"]) + t_width * coarse_t_index
            t_upper = float(target["t_lower"]) + t_width * (
                coarse_t_index + 1
            )
            leaf_rows, local_evaluations = refine_t_cell(
                parent,
                configuration,
                cell,
                epsilon,
                displacement,
                target_path,
                x_index,
                coarse_t_index,
                x_lower,
                x_upper,
                t_lower,
                t_upper,
                0,
                "",
            )
            rows.extend(leaf_rows)
            evaluation_count += local_evaluations
        print(
            json.dumps(
                {
                    "state": "endpoint_negative_real_progress",
                    "target": target_path,
                    "x_slabs_completed": x_index + 1,
                    "x_slab_count": x_count,
                    "evaluation_count": evaluation_count,
                }
            ),
            flush=True,
        )
    target_hull = hull_bounds(rows)
    failed_count = sum(not bool(row["cell_passed"]) for row in rows)
    ratio_abs_upper = float(ratio_row["maximum_ratio_abs_upper"])
    square_edge_abs_upper = 1.0 + ratio_abs_upper
    reciprocal_abs_upper = (
        square_edge_abs_upper / target_hull["invariant_abs_lower"]
        if target_hull["invariant_abs_lower"] > 0.0
        else math.inf
    )
    epsilon_real_lower, epsilon_real_upper = parent.M5394.real_bounds(epsilon)
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        parent.M5394.imaginary_bounds(epsilon)
    )
    summary = {
        "checkpoint": CHECKPOINT,
        **target,
        "parent_revision": parent.REVISION,
        "mapped_cell_id": cell["mapped_cell_id"],
        "configuration_role": configuration["role"],
        "soft_sign": configuration["soft_sign"],
        "decay_sign": configuration["decay_sign"],
        "epsilon_real_lower": epsilon_real_lower,
        "epsilon_real_upper": epsilon_real_upper,
        "epsilon_imaginary_lower": epsilon_imaginary_lower,
        "epsilon_imaginary_upper": epsilon_imaginary_upper,
        "global_displacement_radius": displacement_radius,
        "x_subdivision_count": x_count,
        "coarse_t_subdivision_count": COARSE_T_SUBDIVISION_COUNT,
        "endpoint_coarse_t_count": ENDPOINT_COARSE_T_COUNT,
        "maximum_t_refinement_depth": MAXIMUM_T_REFINEMENT_DEPTH,
        "minimum_t_width": t_width / 2.0**MAXIMUM_T_REFINEMENT_DEPTH,
        "evaluation_count": evaluation_count,
        "cover_leaf_count": len(rows),
        "tail_hull_count": COARSE_T_SUBDIVISION_COUNT
        - ENDPOINT_COARSE_T_COUNT,
        "failed_leaf_count": failed_count,
        **target_hull,
        "representative_ratio_abs_upper": ratio_abs_upper,
        "square_edge_abs_upper": square_edge_abs_upper,
        "external01_reciprocal_abs_upper": reciprocal_abs_upper,
        "reciprocal_identity": "1/<01> = [01]/s01",
        "valid_for_external01_negative_real_invariant_subcover": (
            failed_count == 0
            and target_hull["invariant_real_upper"] < 0.0
            and target_hull["invariant_abs_lower"] > 0.0
            and math.isfinite(reciprocal_abs_upper)
        ),
        **{flag: False for flag in BROAD_FLAGS},
    }
    return rows, summary


def write_document(payload: dict[str, Any], summaries: list[dict[str, Any]]) -> None:
    if payload["valid_for_external01_negative_real_invariant_subcover"]:
        decision = "**PASS FOR THE REPRESENTATIVE EXTERNAL01 INVARIANT SUBCOVER ONLY.**"
        interpretation = (
            "The broad LR/R representative family has a finite negative-real "
            "subcover for `s01`. The pointwise endpoint is regular, the first nine "
            "coarse `t` cells close after adaptive refinement no deeper than "
            "`1/2048`, and the existing tail remains negative-real. Combined with "
            "the already-proved ratio disk, the exact identity "
            "`1/<01> = [01]/s01` gives a finite reciprocal bound without inventing "
            "an independent angle-edge closure."
        )
    else:
        decision = "**ENDPOINT INVARIANT SUBCOVER REMAINS OPEN.**"
        interpretation = (
            "At least one refined leaf or target hull still reaches zero; v47 "
            "remains unchanged."
        )
    lines = [
        "# 5438: anisotropic endpoint-t negative-real invariant subcover gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        interpretation,
        "",
        "## Certified cover",
        "",
        "| target | x slabs | evaluations | leaves | max Re(s01) | min |s01| | max |1/<01>| |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summaries:
        lines.append(
            "| {refinement_path} | {x_subdivision_count} | {evaluation_count} | "
            "{cover_leaf_count} | {invariant_real_upper:.12g} | "
            "{invariant_abs_lower:.12g} | "
            "{external01_reciprocal_abs_upper:.12g} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Construction",
            "",
            "- Keep the 5436 coarse tail `t >= 9/128`, whose union is already strictly negative-real.",
            "- Cover LR with 8 `x` slabs and R with 32 `x` slabs.",
            "- Adaptively bisect only the first nine coarse `t` cells, to maximum depth four (`Delta t = 1/2048`).",
            "- Hull all leaves in the common negative-real half-plane.",
            "- Use `|1/<01>| <= (1 + sup|R01|) / inf|s01|`, sourced from `[01] = R01 - 1` and `s01 = <01>[01]`.",
            "",
            "## Scope",
            "",
            "The declared regulator and contour-displacement boxes remain intact. This gate certifies one representative right-connector reciprocal family only. Parent v47 is unchanged and every broader claim flag remains false.",
            "",
            "## Next target",
            "",
            "Install the adaptive invariant subcover as parent v48, dry-run, migrate the saved state, and resume briefly to verify that the c0 external01 failure count stops increasing.",
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    parent = load_module("mts_5396_v47_for_5438", PARENT_SCRIPT)
    utility = load_module("mts_5428_for_5438", UTILITY_SCRIPT)
    isotropic = load_module("mts_5434_for_5438", ISOTROPIC_SCRIPT)
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    ratio_rows = read_csv(RATIO_SUMMARY)
    ratio_result = json.loads(RATIO_RESULT.read_text(encoding="utf-8"))
    previous_rows = read_csv(PREVIOUS_ROWS)
    previous_result = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    pointwise_result = json.loads(
        POINTWISE_RESULT.read_text(encoding="utf-8")
    )
    pointwise_validation = read_csv(POINTWISE_VALIDATION)
    state_before = ACTIVE_STATE.read_bytes()
    rows_before = ACTIVE_ROWS.read_bytes()
    cell, epsilon_row = isotropic.epsilon_and_cell(parent)
    epsilon = parent.epsilon_interval(epsilon_row)
    targets = isotropic.targets(utility)
    all_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for target in sorted(targets, key=lambda row: row["refinement_path"]):
        target_path = str(target["refinement_path"])
        source_rows = [
            row for row in previous_rows if row["target_path"] == target_path
        ]
        ratio_row = next(
            row for row in ratio_rows if row["refinement_path"] == target_path
        )
        rows, summary = cover_target(
            parent,
            isotropic,
            cell,
            epsilon,
            target,
            source_rows,
            ratio_row,
        )
        all_rows.extend(rows)
        summaries.append(summary)
        atomic_csv(COVER_ROWS, all_rows)
        atomic_csv(SUMMARY_ROWS, summaries)
    all_passed = len(summaries) == 2 and all(
        bool(row["valid_for_external01_negative_real_invariant_subcover"])
        for row in summaries
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "source_cell_count": len(previous_rows),
        "target_count": len(summaries),
        "evaluation_count": sum(
            int(row["evaluation_count"]) for row in summaries
        ),
        "cover_leaf_count": len(all_rows),
        "failed_leaf_count": sum(
            int(row["failed_leaf_count"]) for row in summaries
        ),
        "maximum_invariant_real_upper": max(
            float(row["invariant_real_upper"]) for row in summaries
        ),
        "minimum_invariant_abs_lower": min(
            float(row["invariant_abs_lower"]) for row in summaries
        ),
        "maximum_external01_reciprocal_abs_upper": max(
            float(row["external01_reciprocal_abs_upper"])
            for row in summaries
        ),
        "valid_for_external01_negative_real_invariant_subcover": all_passed,
        "next_target": (
            "PARENT_V48_REPRESENTATIVE_EXTERNAL01_INVARIANT_SUBCOVER_INTEGRATION"
            if all_passed
            else "DEEPER_ENDPOINT_T_OR_X_REFINEMENT"
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
    nonnegative_previous_count = sum(
        float(row["invariant_real_upper"]) >= 0.0 for row in previous_rows
    )
    validations = [
        validation_row(
            "all_sources_exist",
            all(
                path.exists()
                for path in (
                    PARENT_SCRIPT,
                    UTILITY_SCRIPT,
                    ISOTROPIC_SCRIPT,
                    RATIO_SUMMARY,
                    RATIO_RESULT,
                    PREVIOUS_ROWS,
                    PREVIOUS_RESULT,
                    POINTWISE_RESULT,
                    POINTWISE_VALIDATION,
                    ACTIVE_STATE,
                    ACTIVE_ROWS,
                )
            ),
            "eleven local inputs",
        ),
        validation_row(
            "parent_revision_is_v47",
            parent.REVISION == PARENT_REVISION,
            parent.REVISION,
        ),
        validation_row(
            "ratio_disk_gate_is_green",
            int(ratio_result["failed_validation_count"]) == 0
            and bool(ratio_result["valid_for_anisotropic_mirror_disk_cover"]),
            f"rows={len(ratio_rows)}",
        ),
        validation_row(
            "pointwise_finite_endpoint_is_green",
            int(pointwise_result["failed_validation_count"]) == 0
            and bool(pointwise_result["pointwise_finite_endpoint_detected"])
            and all(row["passed"] == "True" for row in pointwise_validation),
            f"rows={len(pointwise_validation)}",
        ),
        validation_row(
            "5436_failure_topology_matches",
            len(previous_rows) == EXPECTED_PREVIOUS_CELL_COUNT
            and int(previous_result["failed_cell_count"])
            == EXPECTED_PREVIOUS_FAILED_COUNT
            and nonnegative_previous_count == EXPECTED_NONNEGATIVE_REAL_COUNT,
            (
                f"cells={len(previous_rows)}, failed={previous_result['failed_cell_count']}, "
                f"nonnegative real={nonnegative_previous_count}"
            ),
        ),
        validation_row(
            "all_adaptive_leaves_are_negative_real",
            all_passed and payload["failed_leaf_count"] == 0,
            f"failed leaves={payload['failed_leaf_count']}",
        ),
        validation_row(
            "common_invariant_hulls_exclude_zero",
            payload["maximum_invariant_real_upper"] < 0.0
            and payload["minimum_invariant_abs_lower"] > 0.0,
            (
                f"max real={payload['maximum_invariant_real_upper']}, "
                f"min abs={payload['minimum_invariant_abs_lower']}"
            ),
        ),
        validation_row(
            "reciprocal_bounds_are_finite",
            math.isfinite(payload["maximum_external01_reciprocal_abs_upper"]),
            str(payload["maximum_external01_reciprocal_abs_upper"]),
        ),
        validation_row(
            "active_parent_state_unchanged",
            state_unchanged,
            str(ACTIVE_STATE),
        ),
        validation_row(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"touches={len(formalization_touches)}",
        ),
        validation_row(
            "broad_claim_flags_false",
            not any(bool(payload[flag]) for flag in BROAD_FLAGS),
            "all broad flags false",
        ),
    ]
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    payload["elapsed_seconds"] = (
        datetime.now(timezone.utc) - started
    ).total_seconds()
    atomic_csv(COVER_ROWS, all_rows)
    atomic_csv(SUMMARY_ROWS, summaries)
    atomic_csv(VALIDATION, validations)
    atomic_json(RESULT, payload)
    write_document(payload, summaries)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    result = run_gate()
    raise SystemExit(0 if result["failed_validation_count"] == 0 else 1)
