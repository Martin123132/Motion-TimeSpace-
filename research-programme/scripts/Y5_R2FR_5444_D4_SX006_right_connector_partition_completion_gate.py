from __future__ import annotations

import csv
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


CHECKPOINT = 5444
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
PARTS = FUNCTIONAL_RG / "5396" / "partial" / "path_parts"
TARGET_STEM = "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR"
TARGET_CSV = PARTS / f"{TARGET_STEM}.csv"
TARGET_PARTITION_CSV = (
    PARTS / "_partitions" / f"{TARGET_STEM}_part_00_of_01.csv"
)
TARGET_STATE = (
    PARTS / "_partitions" / f"{TARGET_STEM}_part_00_of_01.state.json"
)
STATUS = FUNCTIONAL_RG / "5396" / "status.json"
PRE_STATE = OUTPUT / "v49_pre_resume_state.json"
MID_STATE = OUTPUT / "v49_mid_resume_state.json"
LATE_STATE = OUTPUT / "v49_late_resume_state.json"
FINAL_STATE = OUTPUT / "v49_final_resume_state.json"
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5443" / "parent_v49_right_connector_bounded_resume_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5443" / "P8_Y5_BRR5396_5443_VALIDATION.csv"
)
DOCUMENT = POST / "5444-Y5-R2FR-D4-SX006-right-connector-partition-completion-gate.md"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5444_VALIDATION.csv"
RESULT = OUTPUT / "SX006_right_connector_partition_completion_result.json"

EXPECTED_REVISION = "D4-deformed-contour-regular-away-W3-v49"
MAPPED_CELL_ID = "S_X006_MC04_SP_DP"
TERM_ID = "MC04_SP_DP"
PATH_SEGMENT = "RIGHT_CONNECTOR"
MAXIMUM_DEPTH = 18
BROAD_FLAGS = (
    "valid_for_all_right_connector_completion",
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "check": name,
        "passed": passed,
        "detail": detail,
    }


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths)
    return all(
        not right.startswith(left)
        for left, right in zip(ordered, ordered[1:])
    )


def write_document(payload: dict[str, Any]) -> None:
    decision = (
        "**THE S_X006 MC04_SP_DP RIGHT-CONNECTOR PARTITION IS COMPLETE.**"
        if payload["valid_for_SX006_right_connector_partition_completion"]
        else "**THE S_X006 RIGHT-CONNECTOR PARTITION REMAINS OPEN.**"
    )
    lines = [
        "# 5444: S_X006 right-connector partition completion gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        "Parent v49 exhausted the adaptive stack for regulator slab `bin_00/sub_00` and wrote the completed path CSV. This closes the exact production branch that exposed the external01 and collision-Jacobian enclosure failures repaired in checkpoints 5438-5441.",
        "",
        "## Certified cover",
        "",
        f"- Leaves: `{payload['certified_leaf_count']}`.",
        f"- Domain: `x in [{payload['x_lower']}, {payload['x_upper']}]`, `t in [0,1]`.",
        f"- Prefix-free Kraft sum: `{payload['kraft_sum']}`.",
        f"- Parameter-area sum: `{payload['parameter_area_sum']}` against expected `{payload['expected_parameter_area']}`.",
        f"- Maximum refinement depth: `{payload['maximum_refinement_depth']}` of `{MAXIMUM_DEPTH}`.",
        f"- Minimum amplitude denominator: `{payload['minimum_amplitude_denominator_abs_lower']}`.",
        f"- Minimum collision Jacobian: `{payload['minimum_collision_jacobian_abs_lower']}`.",
        "",
        "## Production transition",
        "",
        f"- Accepted count at v49 integration: `{payload['integration_start_accepted_count']}`.",
        f"- Final completed leaf count: `{payload['certified_leaf_count']}`.",
        f"- The target state file is removed: `{payload['target_state_removed']}`.",
        f"- Parent advanced to `{payload['next_active_state_name']}`.",
        "",
        "## Claim boundary",
        "",
        "This is a genuine finite-cover completion for one mapped cell, path segment, and regulator slab. Other path jobs and the second regulator slab remain; no all-right-connector, regular-away W3, UV, local-GR, or full-MTS claim is made.",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    parent = load_module("mts_parent_5396_v49_for_5444", PARENT_SCRIPT)
    parent.iv.dps = parent.INTERVAL_DIGITS
    previous = read_json(PREVIOUS_RESULT)
    previous_validation = read_csv(PREVIOUS_VALIDATION)
    status = read_json(STATUS)
    snapshots = [
        read_json(path)
        for path in (PRE_STATE, MID_STATE, LATE_STATE, FINAL_STATE)
    ]
    rows = read_csv(TARGET_CSV)
    partition_rows = read_csv(TARGET_PARTITION_CSV)
    cell = next(
        row
        for row in parent.away_term_support_cells()
        if row["mapped_cell_id"] == MAPPED_CELL_ID
    )
    x_lower = float(cell["lower_absolute_soft_cosine"])
    x_upper = float(cell["upper_absolute_soft_cosine"])
    expected_area = x_upper - x_lower
    paths = [row["refinement_path"] for row in rows]
    depths = [int(row["refinement_depth"]) for row in rows]
    areas = [float(row["parameter_area"]) for row in rows]
    area_sum = math.fsum(areas)
    kraft_sum = math.fsum(2.0 ** (-depth) for depth in depths)
    path_geometry_exact = all(
        len(path) == depth
        and math.isclose(
            area,
            expected_area * 2.0 ** (-depth),
            rel_tol=3.0e-12,
            abs_tol=3.0e-18,
        )
        for path, depth, area in zip(paths, depths, areas)
    )
    active_states = list(PARTS.rglob("*.state.json"))
    active_state_data = [read_json(path) for path in active_states]
    minimum_amplitude = min(
        float(row["minimum_amplitude_denominator_abs_lower"])
        for row in rows
    )
    minimum_collision = min(
        float(row["collision_jacobian_abs_lower"]) for row in rows
    )
    maximum_depth = max(depths)
    finite_rows = all(
        math.isfinite(float(row["integrated_regular_path_abs_upper"]))
        and float(row["integrated_regular_path_abs_upper"]) >= 0.0
        and float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
        and float(row["collision_jacobian_abs_lower"]) > 0.0
        for row in rows
    )
    cover_complete = (
        len(rows) == 735
        and len(paths) == len(set(paths))
        and prefix_free(paths)
        and path_geometry_exact
        and math.isclose(kraft_sum, 1.0, rel_tol=0.0, abs_tol=2.0e-14)
        and math.isclose(area_sum, expected_area, rel_tol=0.0, abs_tol=2.0e-14)
        and finite_rows
        and maximum_depth < MAXIMUM_DEPTH
        and not TARGET_STATE.exists()
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "mapped_cell_id": MAPPED_CELL_ID,
        "term_id": TERM_ID,
        "path_segment": PATH_SEGMENT,
        "regulator_bin_index": 0,
        "epsilon_subdivision_index": 0,
        "certified_leaf_count": len(rows),
        "integration_start_accepted_count": int(snapshots[0]["accepted_count"]),
        "x_lower": x_lower,
        "x_upper": x_upper,
        "expected_parameter_area": expected_area,
        "parameter_area_sum": area_sum,
        "kraft_sum": kraft_sum,
        "prefix_free": prefix_free(paths),
        "path_geometry_exact": path_geometry_exact,
        "maximum_refinement_depth": maximum_depth,
        "minimum_amplitude_denominator_abs_lower": minimum_amplitude,
        "minimum_collision_jacobian_abs_lower": minimum_collision,
        "target_and_partition_csv_sha256_match": (
            sha256(TARGET_CSV) == sha256(TARGET_PARTITION_CSV)
        ),
        "target_state_removed": not TARGET_STATE.exists(),
        "active_state_count": len(active_states),
        "next_active_state_name": (
            active_states[0].name if len(active_states) == 1 else ""
        ),
        "next_active_state_accepted_count": (
            int(active_state_data[0]["accepted_count"])
            if len(active_state_data) == 1
            else -1
        ),
        "next_active_state_pending_count": (
            len(active_state_data[0]["stack"])
            if len(active_state_data) == 1
            else -1
        ),
        "runner_state": status["state"],
        "runner_resume_safe": bool(status["resume_safe"]),
        "valid_for_SX006_right_connector_partition_completion": (
            cover_complete
        ),
        "valid_for_parent_v49_repaired_branch_completion": cover_complete,
        "next_target": "CONTINUE_PARENT_V49_FROM_SX007_TOP",
        **{flag: False for flag in BROAD_FLAGS},
    }
    validations = [
        check(
            "all_sources_exist",
            all(
                path.exists()
                for path in (
                    PARENT_SCRIPT,
                    TARGET_CSV,
                    TARGET_PARTITION_CSV,
                    STATUS,
                    PRE_STATE,
                    MID_STATE,
                    LATE_STATE,
                    FINAL_STATE,
                    PREVIOUS_RESULT,
                    PREVIOUS_VALIDATION,
                )
            ),
            "ten local inputs",
        ),
        check(
            "checkpoint_5443_is_green",
            int(previous["failed_validation_count"]) == 0
            and bool(previous["valid_for_parent_v49_bounded_resume_progress"])
            and all(row["passed"] == "True" for row in previous_validation),
            f"rows={len(previous_validation)}",
        ),
        check(
            "parent_and_snapshots_are_v49",
            parent.REVISION == EXPECTED_REVISION
            and all(row["revision"] == EXPECTED_REVISION for row in snapshots),
            parent.REVISION,
        ),
        check(
            "completed_csvs_are_identical",
            payload["target_and_partition_csv_sha256_match"],
            f"rows={len(rows)}",
        ),
        check(
            "leaf_paths_are_unique_and_prefix_free",
            len(paths) == len(set(paths)) and prefix_free(paths),
            f"paths={len(paths)}",
        ),
        check(
            "dyadic_leaf_geometry_matches_paths",
            path_geometry_exact,
            f"maximum_depth={maximum_depth}",
        ),
        check(
            "kraft_sum_proves_complete_partition_tree",
            math.isclose(kraft_sum, 1.0, rel_tol=0.0, abs_tol=2.0e-14),
            str(kraft_sum),
        ),
        check(
            "parameter_area_matches_full_domain",
            math.isclose(area_sum, expected_area, rel_tol=0.0, abs_tol=2.0e-14),
            f"sum={area_sum}, expected={expected_area}",
        ),
        check(
            "all_leaf_bounds_are_finite_and_positive",
            finite_rows and minimum_amplitude > 0.0 and minimum_collision > 0.0,
            f"amplitude={minimum_amplitude}, collision={minimum_collision}",
        ),
        check(
            "completion_occurs_below_maximum_depth",
            maximum_depth < MAXIMUM_DEPTH,
            f"depth={maximum_depth}/{MAXIMUM_DEPTH}",
        ),
        check(
            "target_state_is_exhausted_and_removed",
            not TARGET_STATE.exists(),
            str(TARGET_STATE),
        ),
        check(
            "parent_advanced_resume_safely",
            len(active_states) == 1
            and MAPPED_CELL_ID not in active_states[0].name
            and status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"]),
            payload["next_active_state_name"],
        ),
        check(
            "partition_completion_gate_passes",
            cover_complete,
            "735-leaf finite cover is complete",
        ),
        check(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_FLAGS),
            "other path jobs and regulator slab remain",
        ),
    ]
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations.append(
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"modified_file_count={len(formalization_touches)}",
        )
    )
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    atomic_csv(VALIDATION, validations)
    write_document(payload)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run_gate()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
