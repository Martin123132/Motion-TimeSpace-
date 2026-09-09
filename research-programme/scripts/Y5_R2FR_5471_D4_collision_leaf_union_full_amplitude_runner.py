from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
FORMALIZATION = POST.parent / "formalization-workbench"
OUTPUT = FUNCTIONAL_RG / "5471"
WORK = OUTPUT / "work-v1"

SCRIPT_5470 = SCRIPTS / "Y5_R2FR_5470_D4_unresolved_cuboid_collision_jacobian_leaf_union_gate.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
RESULT_5470 = FUNCTIONAL_RG / "5470" / "D4_unresolved_collision_jacobian_leaf_union_result.json"
VALIDATION_5470 = FUNCTIONAL_RG / "5470" / "P8_Y5_BRR5469_5470_VALIDATION.csv"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE_5469 = FUNCTIONAL_RG / "5469" / "work-v1" / f"{TARGET_CUBOID_ID}.json"
TARGET_SNAPSHOT_5470 = FUNCTIONAL_RG / "5470" / "target_unresolved_node_snapshot.json"

LEAF_MANIFEST = OUTPUT / "D4_collision_leaf_union_full_amplitude_manifest.csv"
CERTIFICATES = OUTPUT / "D4_collision_leaf_union_full_amplitude_certificates.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5470_5471_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_collision_leaf_union_full_amplitude_result.json"
REPAIR_CERTIFICATE = OUTPUT / "D4_unresolved_subcuboid_repair_certificate.json"
DOCUMENT = POST / "5471-Y5-R2FR-D4-collision-leaf-union-full-amplitude-runner.md"

CHECKPOINT = 5471
REVISION = "D4-collision-leaf-union-full-amplitude-runner-v2"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def truth(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5470,
        SCRIPT_5469,
        SCRIPT_5468,
        RESULT_5470,
        VALIDATION_5470,
        MANIFEST_5468,
        TARGET_SNAPSHOT_5470,
    )


def leaf_manifest(
    unresolved: dict[str, Any], t_count: int
) -> list[dict[str, Any]]:
    t_lower = float(unresolved["t_lower"])
    t_upper = float(unresolved["t_upper"])
    width = (t_upper - t_lower) / t_count
    additional_depth = int(math.log2(t_count))
    if 2**additional_depth != t_count:
        raise ValueError("selected t cover must be dyadic")
    rows: list[dict[str, Any]] = []
    for index in range(t_count):
        rows.append(
            {
                "leaf_id": f"T{index:03d}_OF_{t_count:03d}",
                "leaf_index": index,
                "leaf_count": t_count,
                "epsilon_real_lower": float(unresolved["epsilon_real_lower"]),
                "epsilon_real_upper": float(unresolved["epsilon_real_upper"]),
                "x_lower": float(unresolved["x_lower"]),
                "x_upper": float(unresolved["x_upper"]),
                "t_lower": t_lower + index * width,
                "t_upper": t_lower + (index + 1) * width,
                "refinement_depth": int(unresolved["refinement_depth"])
                + additional_depth,
                "refinement_path": (
                    f"{unresolved['refinement_path']}_JACOBIAN_T{index:03d}"
                ),
                "exact_leaf_of_selected_jacobian_union": True,
                "valid_for_full_amplitude_leaf": False,
                "valid_for_unresolved_subcuboid_repair": False,
                "valid_for_full_outer_parent_leaf_enclosure": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5471: D4 collision leaf-union full-amplitude runner",
        "",
        "## Construction",
        "",
        "Checkpoint 5470 proves that the unresolved collision-Jacobian box is pointwise regular and that a path-only 128-leaf union separates every selected Jacobian and projective denominator from zero. This runner applies the unchanged parent-v51 full-amplitude evaluator to those exact same leaves. Each leaf is committed atomically, so interruption loses at most the active leaf.",
        "",
        "## Current state",
        "",
        f"Passed leaves: `{payload['passed_leaf_count']}/{payload['expected_leaf_count']}`. Failed leaves: `{payload['failed_leaf_count']}`. Remaining leaves: `{payload['remaining_leaf_count']}`.",
        "",
        f"Minimum amplitude denominator: `{payload['minimum_amplitude_denominator_abs_lower']}`. Minimum collision Jacobian: `{payload['minimum_collision_jacobian_abs_lower']}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "Only a complete 128/128 pass repairs the one checkpoint-5469 unresolved subcuboid. The parent cuboid still has pending siblings afterward; full outer enclosure, W3, the regulator limit, local GR and full MTS remain unclaimed.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def run(maximum_leaves: int, status_only: bool) -> dict[str, Any]:
    base_5469 = load_module("mts_5469_for_5471", SCRIPT_5469)
    base_5468 = load_module("mts_5468_for_5471", SCRIPT_5468)
    base_5467 = base_5468.load_module("mts_5467_for_5471", base_5468.SCRIPT_5467)
    base_5467.set_below_normal_priority()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5470 = read_json(RESULT_5470)
    validation_5470 = read_csv(VALIDATION_5470)
    snapshot = read_json(TARGET_SNAPSHOT_5470)
    unresolved = snapshot["unresolved_node"]
    selected_cover = result_5470["selected_cover"]
    if int(selected_cover["x_count"]) != 1:
        raise RuntimeError("checkpoint 5471 currently owns path-only covers")
    expected_leaf_count = int(selected_cover["t_count"])
    leaves = leaf_manifest(unresolved, expected_leaf_count)
    base_5467.atomic_csv(LEAF_MANIFEST, leaves)
    manifest_by_id = {
        row["cuboid_job_id"]: row for row in read_csv(MANIFEST_5468)
    }
    cuboid = manifest_by_id[TARGET_CUBOID_ID]
    WORK.mkdir(parents=True, exist_ok=True)
    completed_ids = {path.stem for path in WORK.glob("*.json") if path.is_file()}
    pending = [row for row in leaves if row["leaf_id"] not in completed_ids]
    processed = 0
    if pending and not status_only:
        stable, parent, cells, support_segments, branches = base_5467.load_parent()
        if parent.REVISION != PARENT_REVISION:
            raise RuntimeError(
                f"expected parent revision {PARENT_REVISION}, found {parent.REVISION}"
            )
        for leaf in pending:
            if processed >= maximum_leaves:
                break
            result = base_5469.evaluate_node(
                base_5468,
                stable,
                parent,
                cells,
                support_segments,
                branches,
                cuboid,
                leaf,
            )
            compact = base_5469.compact_node_result(leaf, result)
            compact.update(
                {
                    "leaf_id": leaf["leaf_id"],
                    "certificate_source": "checkpoint_5471_parent_v51_on_5470_jacobian_leaf_union",
                    "parent_revision": PARENT_REVISION,
                    "valid_for_full_amplitude_leaf": truth(
                        result.get("probe_passed")
                    ),
                    "valid_for_unresolved_subcuboid_repair": False,
                    "valid_for_full_outer_parent_leaf_enclosure": False,
                    "valid_for_D4_event_local_W3_bound": False,
                    "valid_for_all_operator_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            base_5467.atomic_json(
                WORK / f"{leaf['leaf_id']}.json", compact, compact=True
            )
            processed += 1
            if not truth(compact["valid_for_full_amplitude_leaf"]):
                break
    completed = [
        read_json(WORK / f"{row['leaf_id']}.json")
        for row in leaves
        if (WORK / f"{row['leaf_id']}.json").is_file()
    ]
    passed = [row for row in completed if truth(row["valid_for_full_amplitude_leaf"])]
    failed = [row for row in completed if row not in passed]
    if passed:
        base_5467.atomic_csv(
            CERTIFICATES, sorted(passed, key=lambda row: row["leaf_id"])
        )
    complete = len(passed) == expected_leaf_count and not failed
    original_t_width = float(unresolved["t_upper"]) - float(unresolved["t_lower"])
    covered_t_width = sum(
        float(row["t_upper"]) - float(row["t_lower"]) for row in leaves
    )
    coverage_error = abs(covered_t_width - original_t_width)
    minimum_denominator = min(
        (float(row["minimum_amplitude_denominator_abs_lower"]) for row in passed),
        default=math.nan,
    )
    minimum_jacobian = min(
        (float(row["collision_jacobian_abs_lower"]) for row in passed),
        default=math.nan,
    )
    repair_certificate: dict[str, Any] | None = None
    if complete:
        repair_certificate = {
            "checkpoint": CHECKPOINT,
            "revision": REVISION,
            "target_cuboid_id": TARGET_CUBOID_ID,
            "repaired_refinement_path": unresolved["refinement_path"],
            "repaired_refinement_depth": int(unresolved["refinement_depth"]),
            "replacement_leaf_count": expected_leaf_count,
            "replacement_leaf_ids": [row["leaf_id"] for row in passed],
            "coverage_error": coverage_error,
            "minimum_amplitude_denominator_abs_lower": minimum_denominator,
            "minimum_relative_root_abs_lower": min(
                float(row["relative_root_abs_lower"]) for row in passed
            ),
            "minimum_selected_global_root_abs_lower": min(
                float(row["selected_global_root_abs_lower"]) for row in passed
            ),
            "minimum_collision_jacobian_abs_lower": minimum_jacobian,
            "integrated_regular_path_abs_upper": sum(
                float(row["integrated_regular_path_abs_upper"]) for row in passed
            ),
            "certificate_source": "checkpoint_5470_jacobian_leaf_union_plus_checkpoint_5471_full_amplitude_leaf_union",
            "parent_revision": PARENT_REVISION,
            "valid_for_unresolved_subcuboid_repair": True,
            "valid_for_full_outer_parent_leaf_enclosure": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        base_5467.atomic_json(REPAIR_CERTIFICATE, repair_certificate)
    after_formalization = base_5467.formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "UNRESOLVED_SUBCUBOID_FULL_AMPLITUDE_LEAF_UNION_CERTIFIED__INTEGRATE_REPAIR"
            if complete
            else (
                "FULL_AMPLITUDE_LEAF_FAILURE__REFINE_ONLY_FAILED_LEAF"
                if failed
                else "FULL_AMPLITUDE_LEAF_UNION_PARTIAL__RESUME"
            )
        ),
        "target_cuboid_id": TARGET_CUBOID_ID,
        "expected_leaf_count": expected_leaf_count,
        "completed_leaf_count": len(completed),
        "passed_leaf_count": len(passed),
        "failed_leaf_count": len(failed),
        "remaining_leaf_count": expected_leaf_count - len(passed),
        "processed_this_run": processed,
        "coverage_error": coverage_error,
        "minimum_amplitude_denominator_abs_lower": minimum_denominator,
        "minimum_collision_jacobian_abs_lower": minimum_jacobian,
        "first_failed_leaf_id": failed[0]["leaf_id"] if failed else "",
        "first_failed_leaf_type": failed[0].get("failure_type", "") if failed else "",
        "first_failed_leaf_message": failed[0].get("failure_message", "") if failed else "",
        "valid_for_unresolved_subcuboid_repair": complete,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "INTEGRATE_5471_REPAIR_INTO_5469_RESUME_STATE"
            if complete
            else (failed[0]["leaf_id"] if failed else pending[processed]["leaf_id"] if processed < len(pending) else "")
        ),
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5470_jacobian_leaf_union_is_valid",
            truth(result_5470.get("valid_for_collision_jacobian_leaf_union"))
            and int(result_5470.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5470),
            result_5470.get("decision"),
        ),
        check(
            "selected_128_leaf_path_cover_is_reproduced",
            expected_leaf_count == 128
            and len(leaves) == 128
            and int(selected_cover["x_count"]) == 1,
            len(leaves),
        ),
        check(
            "leaf_union_exactly_covers_unresolved_t_interval",
            coverage_error <= 1.0e-15 * max(original_t_width, 1.0),
            coverage_error,
        ),
        check(
            "all_completed_amplitude_leaves_have_positive_parent_factors",
            all(
                truth(row["valid_for_full_amplitude_leaf"])
                and all(
                    math.isfinite(float(row[field])) and float(row[field]) > 0.0
                    for field in (
                        "minimum_amplitude_denominator_abs_lower",
                        "relative_root_abs_lower",
                        "selected_global_root_abs_lower",
                        "collision_jacobian_abs_lower",
                    )
                )
                for row in passed
            ),
            len(passed),
        ),
        check(
            "failed_or_partial_rows_remain_nonclaim",
            all(
                not truth(row["valid_for_unresolved_subcuboid_repair"])
                and not truth(row["valid_for_full_outer_parent_leaf_enclosure"])
                and not truth(row["valid_for_D4_event_local_W3_bound"])
                and not truth(row["valid_for_all_operator_local_GR_claim"])
                and not truth(row["valid_for_full_MTS_claim"])
                for row in completed
            ),
            len(completed),
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_full_outer_parent_leaf_enclosure"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "one unresolved subcuboid only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    register = [
        {
            "checkpoint": CHECKPOINT,
            "source_path": str(path),
            "sha256": digest(path),
            "exists": path.is_file(),
            "source_role": "collision-leaf-union-amplitude-input",
        }
        for path in source_paths()
    ]
    base_5467.atomic_csv(SOURCE_REGISTER, register)
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-leaves", type=int, default=8)
    parser.add_argument("--status-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_leaves <= 0:
        raise ValueError("--max-leaves must be positive")
    payload = run(arguments.max_leaves, arguments.status_only)
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "passed_leaf_count",
                    "failed_leaf_count",
                    "remaining_leaf_count",
                    "processed_this_run",
                    "minimum_amplitude_denominator_abs_lower",
                    "minimum_collision_jacobian_abs_lower",
                    "next_target",
                    "failed_validation_count",
                )
            },
            indent=2,
        )
    )
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
