from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(variable, "1")


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5467"
WORK = OUTPUT / "work-v1"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5451 = SCRIPTS / "Y5_R2FR_5451_D4_event_endpoint_xt_overlap_geometry_cover.py"
COVER_5451 = FUNCTIONAL_RG / "5451" / "D4_event_endpoint_xt_overlap_cover.csv"
RESULT_5451 = FUNCTIONAL_RG / "5451" / "D4_event_endpoint_xt_overlap_geometry_result.json"
SCRIPT_5456 = SCRIPTS / "Y5_R2FR_5456_D4_outer_parent_leaf_transplant_smoke.py"
SCRIPT_5460 = SCRIPTS / "Y5_R2FR_5460_D4_outer_representative_reconciliation_and_resume.py"
RESULT_5460 = FUNCTIONAL_RG / "5460" / "D4_outer_representative_resume_result.json"
COMBINED_5460 = FUNCTIONAL_RG / "5460" / "D4_outer_representative_combined_results.csv"
VALIDATION_5460 = FUNCTIONAL_RG / "5460" / "P8_Y5_BRR545_5460_VALIDATION.csv"

DOCUMENT = POST / "5467-Y5-R2FR-D4-all-outer-leaf-epsilon-fiber-transplant-runner.md"
MANIFEST = OUTPUT / "D4_outer_leaf_epsilon_fiber_manifest.csv"
CERTIFICATES = OUTPUT / "D4_outer_leaf_epsilon_fiber_certificates.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5460_5467_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_outer_leaf_epsilon_fiber_transplant_result.json"

CHECKPOINT = 5467
REVISION = "D4-all-outer-leaf-epsilon-fiber-transplant-runner-v1"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
EXPECTED_OUTER_SOURCE_LEAF_COUNT = 606_990
EXPECTED_FIBER_COUNT = 99_522
EXPECTED_MULTI_FIBER_SOURCE_LEAF_COUNT = 528_076
EXPECTED_MAXIMUM_FIBER_SOURCE_LEAF_COUNT = 64
OUTER_RADIUS = 5.0e-6

FIBER_KEY_FIELDS = (
    "event_id",
    "event_type",
    "branch_owner_id",
    "mapped_cell_id",
    "term_id",
    "primary_surface_id",
    "epsilon_bin_index",
    "epsilon_subdivision_count",
    "path_segment",
    "x_lower",
    "x_upper",
    "x_width",
    "t_lower",
    "t_upper",
    "t_width",
    "parameter_area",
    "physical_path_area_abs_upper",
    "refinement_depth",
    "refinement_path",
    "path_speed_abs_upper",
    "gap_enclosure_method",
)


def set_below_normal_priority() -> None:
    try:
        ctypes.windll.kernel32.SetPriorityClass(
            ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
        )
    except (AttributeError, OSError):
        pass


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8", newline="\n")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any], compact: bool = False) -> None:
    value = (
        json.dumps(payload, separators=(",", ":"), allow_nan=True) + "\n"
        if compact
        else json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n"
    )
    atomic_text(path, value)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fields: list[str] = []
    known: set[str] = set()
    for row in rows:
        for field in row:
            if field not in known:
                fields.append(field)
                known.add(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


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
        SCRIPT_5451,
        COVER_5451,
        RESULT_5451,
        SCRIPT_5456,
        SCRIPT_5460,
        RESULT_5460,
        COMBINED_5460,
        VALIDATION_5460,
    )


def formalization_snapshot() -> dict[str, tuple[int, int]]:
    if not FORMALIZATION.is_dir():
        return {}
    return {
        str(path.relative_to(FORMALIZATION)): (
            path.stat().st_size,
            path.stat().st_mtime_ns,
        )
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
    }


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=1.0e-13, abs_tol=1.0e-15)


def fiber_identifier(
    key: tuple[str, ...],
    first_index: int,
    last_index: int,
    epsilon_lower: float,
    epsilon_upper: float,
) -> str:
    payload = json.dumps(
        [*key, first_index, last_index, epsilon_lower, epsilon_upper],
        separators=(",", ":"),
    )
    suffix = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"{key[0]}__{key[3]}__{key[8]}__FIBER__{suffix}"


def build_manifest() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    source_leaf_count = 0
    source_outer_gap_failure_count = 0
    source_nonfinite_geometry_count = 0
    with COVER_5451.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["cover_owner"] != "OUTER_PARENT_TRIANGLE":
                continue
            source_leaf_count += 1
            gap_lower = float(row["gap_abs_lower"])
            physical_area = float(row["physical_path_area_abs_upper"])
            if gap_lower < OUTER_RADIUS:
                source_outer_gap_failure_count += 1
            if not all(
                math.isfinite(value) and value >= 0.0
                for value in (gap_lower, physical_area)
            ):
                source_nonfinite_geometry_count += 1
            key = tuple(row[field] for field in FIBER_KEY_FIELDS)
            groups[key].append(
                {
                    "index": int(row["epsilon_subdivision_index"]),
                    "epsilon_real_lower": float(row["epsilon_real_lower"]),
                    "epsilon_real_upper": float(row["epsilon_real_upper"]),
                    "epsilon_imaginary_lower": float(
                        row["epsilon_imaginary_lower"]
                    ),
                    "epsilon_imaginary_upper": float(
                        row["epsilon_imaginary_upper"]
                    ),
                    "gap_abs_lower": gap_lower,
                    "gap_abs_upper": float(row["gap_abs_upper"]),
                    "material_root_denominator_abs_lower": float(
                        row["material_root_denominator_abs_lower"]
                    ),
                    "implicit_material_derivative_abs_lower": float(
                        row["implicit_material_derivative_abs_lower"]
                    ),
                }
            )

    duplicate_source_identity_count = 0
    noncontiguous_union_count = 0
    manifest: list[dict[str, Any]] = []

    def append_run(key: tuple[str, ...], run: list[dict[str, Any]]) -> None:
        nonlocal noncontiguous_union_count
        first = run[0]
        last = run[-1]
        exact_union = all(
            right["index"] == left["index"] + 1
            and close(
                right["epsilon_real_lower"], left["epsilon_real_upper"]
            )
            and close(
                right["epsilon_imaginary_lower"],
                left["epsilon_imaginary_lower"],
            )
            and close(
                right["epsilon_imaginary_upper"],
                left["epsilon_imaginary_upper"],
            )
            for left, right in zip(run[:-1], run[1:])
        )
        if not exact_union:
            noncontiguous_union_count += 1
        source = dict(zip(FIBER_KEY_FIELDS, key))
        job_id = fiber_identifier(
            key,
            first["index"],
            last["index"],
            first["epsilon_real_lower"],
            last["epsilon_real_upper"],
        )
        manifest.append(
            {
                "fiber_job_id": job_id,
                **source,
                "source_subdivision_index_lower": first["index"],
                "source_subdivision_index_upper": last["index"],
                "source_leaf_count": len(run),
                "epsilon_real_lower": first["epsilon_real_lower"],
                "epsilon_real_upper": last["epsilon_real_upper"],
                "epsilon_imaginary_lower": first[
                    "epsilon_imaginary_lower"
                ],
                "epsilon_imaginary_upper": first[
                    "epsilon_imaginary_upper"
                ],
                "source_partition_minimum_gap_abs_lower": min(
                    row["gap_abs_lower"] for row in run
                ),
                "source_partition_maximum_gap_abs_upper": max(
                    row["gap_abs_upper"] for row in run
                ),
                "source_partition_minimum_material_root_denominator_abs_lower": min(
                    row["material_root_denominator_abs_lower"] for row in run
                ),
                "source_partition_minimum_implicit_material_derivative_abs_lower": min(
                    row["implicit_material_derivative_abs_lower"] for row in run
                ),
                "epsilon_hull_is_exact_contiguous_union": exact_union,
                "transplant_method": "EXACT_CONTIGUOUS_EPSILON_FIBER_HULL_WITH_FIXED_XT_GEOMETRY",
                "valid_for_outer_leaf_epsilon_fiber_transplant": False,
                "valid_for_full_outer_parent_leaf_enclosure": False,
                "valid_for_full_event_cell_finite_cover": False,
                "valid_for_D4_event_local_W3_bound": False,
                "valid_for_all_operator_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )

    for key, entries in sorted(groups.items()):
        ordered = sorted(entries, key=lambda row: row["index"])
        unique: list[dict[str, Any]] = []
        seen_indices: set[int] = set()
        for entry in ordered:
            if entry["index"] in seen_indices:
                duplicate_source_identity_count += 1
                continue
            seen_indices.add(entry["index"])
            unique.append(entry)
        run = [unique[0]]
        for entry in unique[1:]:
            previous = run[-1]
            joins = (
                entry["index"] == previous["index"] + 1
                and close(
                    entry["epsilon_real_lower"],
                    previous["epsilon_real_upper"],
                )
                and close(
                    entry["epsilon_imaginary_lower"],
                    previous["epsilon_imaginary_lower"],
                )
                and close(
                    entry["epsilon_imaginary_upper"],
                    previous["epsilon_imaginary_upper"],
                )
            )
            if joins:
                run.append(entry)
            else:
                append_run(key, run)
                run = [entry]
        append_run(key, run)

    priority = sorted(
        manifest,
        key=lambda row: (
            -int(row["source_leaf_count"]),
            -float(row["source_partition_minimum_gap_abs_lower"]),
            float(row["physical_path_area_abs_upper"]),
            row["fiber_job_id"],
        ),
    )
    priority_by_id = {
        row["fiber_job_id"]: index + 1 for index, row in enumerate(priority)
    }
    for row in manifest:
        row["evaluation_priority"] = priority_by_id[row["fiber_job_id"]]
    manifest.sort(key=lambda row: int(row["evaluation_priority"]))
    run_lengths = Counter(int(row["source_leaf_count"]) for row in manifest)
    diagnostics = {
        "outer_source_leaf_count": source_leaf_count,
        "fiber_manifest_count": len(manifest),
        "manifest_source_leaf_count": sum(
            int(row["source_leaf_count"]) for row in manifest
        ),
        "multi_fiber_source_leaf_count": sum(
            int(row["source_leaf_count"])
            for row in manifest
            if int(row["source_leaf_count"]) > 1
        ),
        "maximum_fiber_source_leaf_count": max(run_lengths, default=0),
        "compression_factor": source_leaf_count / max(len(manifest), 1),
        "duplicate_source_identity_count": duplicate_source_identity_count,
        "noncontiguous_union_count": noncontiguous_union_count,
        "source_outer_gap_failure_count": source_outer_gap_failure_count,
        "source_nonfinite_geometry_count": source_nonfinite_geometry_count,
        "run_length_histogram": {
            str(length): count for length, count in sorted(run_lengths.items())
        },
    }
    return manifest, diagnostics


def load_parent() -> tuple[Any, Any, dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    stable = load_module("mts_5456_for_5467", SCRIPT_5456)
    module_5449 = stable.load_module("mts_5449_for_5467", stable.SCRIPT_5449)
    parent = stable.load_module(
        "mts_5396_for_5467", module_5449.PARENT_SCRIPT
    )
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_REVISION}, found {parent.REVISION}"
        )
    parent.set_below_normal_priority()
    stable.install_stable_recoil_sheet(parent)
    cells = {
        row["mapped_cell_id"]: row for row in parent.read_csv(parent.MAPPED_5393)
    }
    return (
        stable,
        parent,
        cells,
        parent.material_support_segments(),
        parent.material_branch_data(),
    )


def evaluate_fiber(
    stable: Any,
    parent: Any,
    cells: dict[str, Any],
    support_segments: list[dict[str, Any]],
    branches: dict[str, Any],
    row: dict[str, Any],
) -> dict[str, Any]:
    probe = {
        "smoke_job_id": row["fiber_job_id"],
        "selection_role": "CONTIGUOUS_EPSILON_FIBER_HULL",
        "event_id": row["event_id"],
        "mapped_cell_id": row["mapped_cell_id"],
        "term_id": row["term_id"],
        "branch_owner_id": row["branch_owner_id"],
        "epsilon_bin_index": int(row["epsilon_bin_index"]),
        "epsilon_subdivision_index": 0,
        "epsilon_subdivision_count": 1,
        "epsilon_real_lower": float(row["epsilon_real_lower"]),
        "epsilon_real_upper": float(row["epsilon_real_upper"]),
        "epsilon_imaginary_lower": float(row["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": float(row["epsilon_imaginary_upper"]),
        "path_segment": row["path_segment"],
        "x_lower": float(row["x_lower"]),
        "x_upper": float(row["x_upper"]),
        "t_lower": float(row["t_lower"]),
        "t_upper": float(row["t_upper"]),
        "refinement_depth": int(row["refinement_depth"]),
        "refinement_path": row["refinement_path"],
        "gap_abs_lower": float(
            row["source_partition_minimum_gap_abs_lower"]
        ),
        "physical_path_area_abs_upper": float(
            row["physical_path_area_abs_upper"]
        ),
    }
    result = stable.adaptive_evaluate_representative(
        parent,
        cells,
        support_segments,
        branches,
        probe,
    )
    passed = truth(result.get("probe_passed"))
    result.update(
        {
            "fiber_job_id": row["fiber_job_id"],
            "source_leaf_count": int(row["source_leaf_count"]),
            "source_subdivision_index_lower": int(
                row["source_subdivision_index_lower"]
            ),
            "source_subdivision_index_upper": int(
                row["source_subdivision_index_upper"]
            ),
            "epsilon_fiber_hull_real_lower": float(
                row["epsilon_real_lower"]
            ),
            "epsilon_fiber_hull_real_upper": float(
                row["epsilon_real_upper"]
            ),
            "epsilon_hull_is_exact_contiguous_union": truth(
                row["epsilon_hull_is_exact_contiguous_union"]
            ),
            "transplant_method": row["transplant_method"],
            "certificate_source": "checkpoint_5467_parent_v51_epsilon_fiber_hull",
            "parent_revision": PARENT_REVISION,
            "valid_for_outer_leaf_epsilon_fiber_transplant": passed,
            "valid_for_full_outer_parent_leaf_enclosure": False,
            "valid_for_full_event_cell_finite_cover": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    return result


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5467: D4 all-outer-leaf epsilon-fiber transplant runner",
        "",
        "## Exact transplant identity",
        "",
        "For a fixed geometry rectangle `(x,t)`, consecutive closed regulator subboxes with matching imaginary interval have an exact union equal to their interval hull. The unchanged parent-v51 interval evaluator run once on that hull therefore encloses every source leaf in the fiber. Geometry ownership is not inferred from a representative margin: every member leaf is already source-certified outer by checkpoint 5451, and the source-partition minimum gap is retained.",
        "",
        "```text",
        "union_j [epsilon_j^-,epsilon_j^+] = [epsilon_a^-,epsilon_b^+]",
        "fixed (x^-,x^+,t^-,t^+) and consecutive j=a,...,b",
        "parent interval certificate on the hull => certificate for all member leaves",
        "```",
        "",
        "A failed hull is an interval-compression failure, not a failed source leaf. It must be split back along its recorded regulator partition or routed through the existing finite projective cover; no representative denominator is transferred.",
        "",
        "## Current state",
        "",
        f"Source outer leaves: `{payload['outer_source_leaf_count']}`. Exact contiguous fibers: `{payload['fiber_manifest_count']}`. Compression factor: `{payload['compression_factor']:.12g}`. Maximum source leaves in one fiber: `{payload['maximum_fiber_source_leaf_count']}`.",
        "",
        f"Certified fibers: `{payload['certified_fiber_count']}/{payload['fiber_manifest_count']}` covering `{payload['certified_source_leaf_count']}/{payload['outer_source_leaf_count']}` source leaves. Failed hull attempts: `{payload['failed_fiber_count']}`. Remaining fibers: `{payload['remaining_fiber_count']}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "The 77/77 representative smoke is complete, but full outer-leaf enclosure becomes true only when every exact fiber is certified or losslessly split to certified children. Event-local W3, the regulator limit, local GR and full MTS remain unclaimed.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run(
    requested_job_id: str | None,
    choose_next: bool,
    max_jobs: int,
    status_only: bool,
    list_next: int,
) -> dict[str, Any]:
    set_below_normal_priority()
    before_formalization = formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5451 = read_json(RESULT_5451)
    result_5460 = read_json(RESULT_5460)
    validation_5460 = read_csv(VALIDATION_5460)
    combined_5460 = read_csv(COMBINED_5460)
    manifest, diagnostics = build_manifest()
    atomic_csv(MANIFEST, manifest)
    manifest_by_id = {row["fiber_job_id"]: row for row in manifest}
    if len(manifest_by_id) != len(manifest):
        raise RuntimeError("fiber job identifiers are not unique")
    WORK.mkdir(parents=True, exist_ok=True)
    completed_ids = {
        path.stem for path in WORK.glob("*.json") if path.is_file()
    }
    pending = [
        row for row in manifest if row["fiber_job_id"] not in completed_ids
    ]
    if list_next > 0:
        print(
            json.dumps(
                [
                    {
                        "fiber_job_id": row["fiber_job_id"],
                        "source_leaf_count": int(row["source_leaf_count"]),
                        "event_id": row["event_id"],
                        "mapped_cell_id": row["mapped_cell_id"],
                        "path_segment": row["path_segment"],
                        "minimum_gap": float(
                            row["source_partition_minimum_gap_abs_lower"]
                        ),
                    }
                    for row in pending[:list_next]
                ],
                indent=2,
            )
        )
    schedule: list[dict[str, Any]] = []
    if requested_job_id:
        if requested_job_id not in manifest_by_id:
            raise ValueError(f"unknown fiber job id: {requested_job_id}")
        if requested_job_id not in completed_ids:
            schedule = [manifest_by_id[requested_job_id]]
    elif choose_next:
        schedule = pending
    if status_only:
        schedule = []
    if schedule and max_jobs <= 0:
        raise ValueError("--max-jobs must be positive when evaluating fibers")
    processed = 0
    if schedule:
        stable, parent, cells, support_segments, branches = load_parent()
        for row in schedule:
            if processed >= max_jobs:
                break
            result = evaluate_fiber(
                stable,
                parent,
                cells,
                support_segments,
                branches,
                row,
            )
            atomic_json(WORK / f"{row['fiber_job_id']}.json", result, compact=True)
            processed += 1
            if not truth(result["valid_for_outer_leaf_epsilon_fiber_transplant"]):
                break

    completed: list[dict[str, Any]] = []
    for row in manifest:
        path = WORK / f"{row['fiber_job_id']}.json"
        if path.is_file():
            completed.append(read_json(path))
    certified = [
        row
        for row in completed
        if truth(row.get("valid_for_outer_leaf_epsilon_fiber_transplant"))
    ]
    failed = [row for row in completed if row not in certified]
    certified_ids = {row["fiber_job_id"] for row in certified}
    certified_source_leaf_count = sum(
        int(row["source_leaf_count"]) for row in certified
    )
    remaining = [
        row for row in manifest if row["fiber_job_id"] not in certified_ids
    ]
    complete = len(certified) == len(manifest) and not failed
    certificates = sorted(certified, key=lambda row: row["fiber_job_id"])
    if certificates:
        atomic_csv(CERTIFICATES, certificates)
    after_formalization = formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "ALL_OUTER_LEAF_EPSILON_FIBER_TRANSPLANT_CERTIFIED__AGGREGATE_INNER_AND_PRINCIPAL"
            if complete
            else (
                "EPSILON_FIBER_HULL_FAILURE__SPLIT_RECORDED_REGULATOR_PARTITION"
                if failed
                else "EPSILON_FIBER_TRANSPLANT_PARTIAL__RESUME"
            )
        ),
        **diagnostics,
        "completed_fiber_count": len(completed),
        "certified_fiber_count": len(certified),
        "failed_fiber_count": len(failed),
        "remaining_fiber_count": len(manifest) - len(certified),
        "certified_source_leaf_count": certified_source_leaf_count,
        "remaining_source_leaf_count": (
            diagnostics["outer_source_leaf_count"]
            - certified_source_leaf_count
        ),
        "processed_this_run": processed,
        "minimum_certified_amplitude_denominator_abs_lower": min(
            (
                float(row["minimum_amplitude_denominator_abs_lower"])
                for row in certified
            ),
            default=math.nan,
        ),
        "first_failed_fiber_job_id": (
            failed[0]["fiber_job_id"] if failed else ""
        ),
        "first_failed_fiber_type": (
            failed[0].get("failure_type", "") if failed else ""
        ),
        "first_failed_fiber_message": (
            failed[0].get("failure_message", "") if failed else ""
        ),
        "next_target": (
            "COMBINE_CERTIFIED_OUTER_WITH_INNER_Q_AND_PRINCIPAL_PART"
            if complete
            else (
                failed[0]["fiber_job_id"]
                if failed
                else (remaining[0]["fiber_job_id"] if remaining else "")
            )
        ),
        "valid_for_outer_leaf_epsilon_fiber_transplant": complete,
        "valid_for_full_outer_parent_leaf_enclosure": complete,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5451_geometry_atlas_is_complete",
            result_5451.get("valid_for_endpoint_xt_overlap_geometry_atlas")
            is True
            and int(result_5451.get("outer_leaf_count", -1))
            == EXPECTED_OUTER_SOURCE_LEAF_COUNT,
            result_5451.get("decision"),
        ),
        check(
            "checkpoint_5460_representative_smoke_is_77_of_77",
            result_5460.get("valid_for_outer_parent_leaf_transplant_smoke")
            is True
            and int(result_5460.get("passed_representative_count", -1)) == 77
            and int(result_5460.get("failed_representative_count", -1)) == 0
            and len(combined_5460) == 77
            and all(truth(row["probe_passed"]) for row in combined_5460)
            and all(truth(row["passed"]) for row in validation_5460),
            result_5460.get("decision"),
        ),
        check(
            "all_606990_outer_source_leaves_are_streamed",
            diagnostics["outer_source_leaf_count"]
            == EXPECTED_OUTER_SOURCE_LEAF_COUNT,
            diagnostics["outer_source_leaf_count"],
        ),
        check(
            "fiber_partition_is_lossless",
            diagnostics["manifest_source_leaf_count"]
            == EXPECTED_OUTER_SOURCE_LEAF_COUNT
            and diagnostics["duplicate_source_identity_count"] == 0,
            diagnostics["manifest_source_leaf_count"],
        ),
        check(
            "all_fiber_hulls_are_exact_contiguous_unions",
            diagnostics["noncontiguous_union_count"] == 0
            and all(
                truth(row["epsilon_hull_is_exact_contiguous_union"])
                for row in manifest
            ),
            diagnostics["noncontiguous_union_count"],
        ),
        check(
            "source_geometry_is_finite_and_outer",
            diagnostics["source_outer_gap_failure_count"] == 0
            and diagnostics["source_nonfinite_geometry_count"] == 0,
            f"gap={diagnostics['source_outer_gap_failure_count']};nonfinite={diagnostics['source_nonfinite_geometry_count']}",
        ),
        check(
            "expected_99522_fiber_manifest_is_reproduced",
            diagnostics["fiber_manifest_count"] == EXPECTED_FIBER_COUNT,
            diagnostics["fiber_manifest_count"],
        ),
        check(
            "expected_multi_fiber_compression_is_reproduced",
            diagnostics["multi_fiber_source_leaf_count"]
            == EXPECTED_MULTI_FIBER_SOURCE_LEAF_COUNT
            and diagnostics["maximum_fiber_source_leaf_count"]
            == EXPECTED_MAXIMUM_FIBER_SOURCE_LEAF_COUNT,
            f"multi={diagnostics['multi_fiber_source_leaf_count']};max={diagnostics['maximum_fiber_source_leaf_count']}",
        ),
        check(
            "all_certified_fibers_have_positive_parent_factors",
            all(
                truth(row["probe_passed"])
                and float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
                and float(row["relative_root_abs_lower"]) > 0.0
                and float(row["selected_global_root_abs_lower"]) > 0.0
                and float(row["collision_jacobian_abs_lower"]) > 0.0
                for row in certified
            ),
            len(certified),
        ),
        check(
            "failed_hull_attempts_remain_nonclaim",
            all(
                not truth(row.get("valid_for_full_outer_parent_leaf_enclosure"))
                and not truth(row.get("valid_for_D4_event_local_W3_bound"))
                and not truth(row.get("valid_for_full_MTS_claim"))
                for row in failed
            ),
            len(failed),
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_full_event_cell_finite_cover"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "outer fiber layer only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    source_rows = [
        {
            "checkpoint": CHECKPOINT,
            "path": str(path.resolve()),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "",
        }
        for path in source_paths()
    ]
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload)
    atomic_json(RESULT, payload)
    atomic_json(STATUS, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id")
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--max-jobs", type=int, default=1)
    parser.add_argument("--status-only", action="store_true")
    parser.add_argument("--list-next", type=int, default=0)
    arguments = parser.parse_args()
    if arguments.job_id and arguments.next:
        raise ValueError("choose either --job-id or --next")
    if arguments.max_jobs < 0 or arguments.list_next < 0:
        raise ValueError("job counts must be nonnegative")
    payload = run(
        arguments.job_id,
        arguments.next,
        arguments.max_jobs,
        arguments.status_only,
        arguments.list_next,
    )
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
