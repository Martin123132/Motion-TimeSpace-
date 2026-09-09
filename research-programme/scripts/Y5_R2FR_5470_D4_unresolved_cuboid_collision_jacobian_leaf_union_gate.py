from __future__ import annotations

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
OUTPUT = FUNCTIONAL_RG / "5470"

SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5440 = SCRIPTS / "Y5_R2FR_5440_D4_collision_jacobian_finite_subcover_gate.py"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"
RESULT_5469 = FUNCTIONAL_RG / "5469" / "D4_resumable_three_axis_cuboid_result.json"
VALIDATION_5469 = FUNCTIONAL_RG / "5469" / "P8_Y5_BRR5468_5469_VALIDATION.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE_5469 = FUNCTIONAL_RG / "5469" / "work-v1" / f"{TARGET_CUBOID_ID}.json"
TARGET_SNAPSHOT = OUTPUT / "target_unresolved_node_snapshot.json"

ABLATIONS = OUTPUT / "D4_unresolved_collision_jacobian_dimension_ablations.csv"
COVER_ROWS = OUTPUT / "D4_unresolved_collision_jacobian_leaf_union_rows.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5469_5470_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_unresolved_collision_jacobian_leaf_union_result.json"
DOCUMENT = POST / "5470-Y5-R2FR-D4-unresolved-cuboid-collision-jacobian-leaf-union-gate.md"

CHECKPOINT = 5470
REVISION = "D4-unresolved-cuboid-collision-jacobian-leaf-union-gate-v3"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
SCHEDULE = (
    (1, 2),
    (1, 4),
    (1, 8),
    (1, 16),
    (1, 32),
    (1, 64),
    (1, 128),
    (1, 256),
)


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
        SCRIPT_5469,
        SCRIPT_5468,
        SCRIPT_5440,
        MANIFEST_5468,
        TARGET_SNAPSHOT,
    )


def configuration_id(index: int, configuration: dict[str, Any]) -> str:
    return f"C{index:02d}_{configuration.get('role', 'unknown')}"


def selected_configurations(
    parent: Any,
    cell: dict[str, Any],
    term_id: str,
    path_segment: str,
    coordinate: Any,
    parameter: Any,
    epsilon: Any,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    lower_energy, _ = parent.interval_boundary_energy(
        cell["lower_energy_boundary"],
        parent.M5394.real_bounds(coordinate)[0],
        parent.M5394.real_bounds(coordinate)[1],
    )
    upper_energy, _ = parent.interval_boundary_energy(
        cell["upper_energy_boundary"],
        parent.M5394.real_bounds(coordinate)[0],
        parent.M5394.real_bounds(coordinate)[1],
    )
    if path_segment == "RIGHT_CONNECTOR":
        energy = upper_energy + parent.cpoint(
            1j * parent.DEFAULT_ENERGY_DEFORMATION
        ) * parameter
    elif path_segment == "LEFT_CONNECTOR":
        energy = lower_energy + parent.cpoint(
            1j * parent.DEFAULT_ENERGY_DEFORMATION
        ) * parameter
    elif path_segment == "TOP":
        energy = lower_energy + parameter * (upper_energy - lower_energy) + parent.cpoint(
            1j * parent.DEFAULT_ENERGY_DEFORMATION
        )
    else:
        raise ValueError(f"unsupported path segment {path_segment}")
    return parent.closed_selector_configuration_subset(
        parent.configuration_variants(term_id),
        coordinate,
        energy,
        epsilon,
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    selected = payload.get("selected_cover") or {}
    lines = [
        "# 5470: D4 unresolved-cuboid collision-Jacobian leaf-union gate",
        "",
        "## Question",
        "",
        "Checkpoint 5469 closes four neighboring depth-24 subcuboids, while one descendant remains unresolved after exact x and epsilon splits. Its relative-root and selected-global-root factors stay positive; only the coarse collision-Jacobian interval reaches zero. The dimension ablation keeps the full x and epsilon boxes nonzero whenever t is fixed, while every test retaining the full t interval remains unresolved. The finite cover therefore refines t only rather than paying for an unmotivated square grid.",
        "",
        "## Exact law",
        "",
        "For a finite cover `D = union_i D_i`, separate interval certificates `0 notin J(D_i)` imply `inf_D |J| >= min_i dist(0,J(D_i)) > 0`. The rectangular hull of all image intervals is not required and may fill gaps that the leaf union does not contain.",
        "",
        "## Result",
        "",
        f"Selected configurations: `{payload['selected_configuration_count']}`. Pointwise-positive configurations: `{payload['pointwise_positive_configuration_count']}`.",
        "",
        f"Selected common cover: `{selected.get('x_count', 'OPEN')} x {selected.get('t_count', 'OPEN')}`. Leaf count per configuration: `{selected.get('leaf_count_per_configuration', 'OPEN')}`. Minimum leaf-union `|J|`: `{selected.get('minimum_leaf_union_abs_lower', 'OPEN')}`. Minimum projective denominator: `{selected.get('minimum_leaf_denominator_abs_lower', 'OPEN')}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "A positive Jacobian leaf union licenses a resume-safe full-amplitude evaluation on the same finite leaves; it does not by itself certify the unresolved subcuboid, the full outer cover, W3, the regulator limit, local GR or full MTS.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5469 = load_module("mts_5469_for_5470", SCRIPT_5469)
    base_5468 = load_module("mts_5468_for_5470", SCRIPT_5468)
    base_5467 = base_5468.load_module("mts_5467_for_5470", base_5468.SCRIPT_5467)
    legacy = load_module("mts_5440_helpers_for_5470", SCRIPT_5440)
    base_5467.set_below_normal_priority()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    snapshot = read_json(TARGET_SNAPSHOT)
    manifest_by_id = {
        row["cuboid_job_id"]: row for row in read_csv(MANIFEST_5468)
    }
    cuboid = manifest_by_id[TARGET_CUBOID_ID]
    node = snapshot["unresolved_node"]
    stable, parent, cells, support_segments, branches = base_5467.load_parent()
    del stable, support_segments, branches
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_REVISION}, found {parent.REVISION}"
        )
    parent.iv.dps = parent.INTERVAL_DIGITS
    coordinate = parent.cbox(float(node["x_lower"]), float(node["x_upper"]))
    parameter = parent.cbox(float(node["t_lower"]), float(node["t_upper"]))
    epsilon = parent.cbox(
        float(node["epsilon_real_lower"]),
        float(node["epsilon_real_upper"]),
        float(cuboid["epsilon_imaginary_lower"]),
        float(cuboid["epsilon_imaginary_upper"]),
    )
    cell = cells[cuboid["mapped_cell_id"]]
    configurations, selector_diagnostics = selected_configurations(
        parent,
        cell,
        cuboid["term_id"],
        cuboid["path_segment"],
        coordinate,
        parameter,
        epsilon,
    )
    configuration_rows = [
        (configuration_id(index, configuration), configuration)
        for index, configuration in enumerate(configurations)
    ]
    ablations: list[dict[str, Any]] = []
    for identifier, configuration in configuration_rows:
        for row in legacy.corrected_ablation(
            parent,
            configuration,
            cell,
            coordinate,
            parameter,
            epsilon,
        ):
            ablations.append({"configuration_id": identifier, **row})
    base_5467.atomic_csv(ABLATIONS, ablations)
    cover_summaries: list[dict[str, Any]] = []
    all_cover_rows: list[dict[str, Any]] = []
    selected_cover: dict[str, Any] | None = None
    for x_count, t_count in SCHEDULE:
        schedule_summaries: list[dict[str, Any]] = []
        schedule_rows: list[dict[str, Any]] = []
        schedule_failed = False
        for identifier, configuration in configuration_rows:
            try:
                summary, rows = legacy.finite_subcover(
                    parent,
                    configuration,
                    cell,
                    coordinate,
                    parameter,
                    epsilon,
                    x_count,
                    t_count,
                )
            except Exception as error:
                summary = {
                    "x_count": x_count,
                    "t_count": t_count,
                    "leaf_count": x_count * t_count,
                    "uncovered_leaf_count": x_count * t_count,
                    "all_leaf_jacobians_nonzero": False,
                    "leaf_union_abs_lower": 0.0,
                    "leaf_denominator_abs_lower": 0.0,
                    "rectangular_hull_abs_lower": 0.0,
                    "error_type": type(error).__name__,
                    "error": str(error).splitlines()[0][:600],
                }
                rows = []
            schedule_summaries.append(
                {"configuration_id": identifier, **summary}
            )
            schedule_rows.extend(
                {"configuration_id": identifier, **row} for row in rows
            )
            if not truth(summary["all_leaf_jacobians_nonzero"]):
                schedule_failed = True
        cover_summaries.extend(schedule_summaries)
        all_cover_rows.extend(schedule_rows)
        if not schedule_failed and schedule_summaries:
            selected_cover = {
                "x_count": x_count,
                "t_count": t_count,
                "leaf_count_per_configuration": x_count * t_count,
                "total_leaf_count": x_count
                * t_count
                * len(configuration_rows),
                "minimum_leaf_union_abs_lower": min(
                    float(row["leaf_union_abs_lower"])
                    for row in schedule_summaries
                ),
                "minimum_leaf_denominator_abs_lower": min(
                    float(row["leaf_denominator_abs_lower"])
                    for row in schedule_summaries
                ),
                "minimum_rectangular_hull_abs_lower": min(
                    float(row["rectangular_hull_abs_lower"])
                    for row in schedule_summaries
                ),
            }
            break
    if all_cover_rows:
        base_5467.atomic_csv(COVER_ROWS, all_cover_rows)
    pointwise_rows = [
        row
        for row in ablations
        if row["x_mode"] == row["t_mode"] == row["epsilon_mode"] == "point"
    ]
    pointwise_positive = [
        row for row in pointwise_rows if float(row["selected_abs_lower"]) > 0.0
    ]
    valid = (
        selected_cover is not None
        and selected_cover["minimum_leaf_union_abs_lower"] > 0.0
        and selected_cover["minimum_leaf_denominator_abs_lower"] > 0.0
    )
    after_formalization = base_5467.formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "COLLISION_JACOBIAN_LEAF_UNION_CERTIFIED__BUILD_RESUMABLE_AMPLITUDE_COVER"
            if valid
            else "COLLISION_JACOBIAN_LEAF_UNION_OPEN__DERIVE_LOCAL_ZERO_OR_REFINE"
        ),
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": node["refinement_path"],
        "target_refinement_depth": int(node["refinement_depth"]),
        "target_failure_type": node["failure_type"],
        "target_failure_message": node["failure_message"],
        "selected_configuration_count": len(configuration_rows),
        "selected_configuration_ids": [row[0] for row in configuration_rows],
        "selector_diagnostics": selector_diagnostics,
        "pointwise_positive_configuration_count": len(pointwise_positive),
        "ablation_row_count": len(ablations),
        "cover_summary_count": len(cover_summaries),
        "cover_row_count": len(all_cover_rows),
        "selected_cover": selected_cover,
        "valid_for_collision_jacobian_leaf_union": valid,
        "valid_for_target_full_amplitude_subcuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "RESUMABLE_FULL_AMPLITUDE_EVALUATION_ON_SELECTED_LEAF_UNION"
            if valid
            else "DISTINGUISH_TRUE_JACOBIAN_ZERO_FROM_INTERVAL_DEPENDENCY"
        ),
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "immutable_checkpoint_5469_target_snapshot_is_valid",
            int(snapshot.get("source_checkpoint", -1)) == 5469
            and snapshot.get("target_cuboid_id") == TARGET_CUBOID_ID
            and truth(snapshot.get("captured_before_checkpoint_5471_integration"))
            and node.get("failure_type") == "EnclosureFailure",
            snapshot.get("snapshot_revision"),
        ),
        check(
            "target_is_collision_jacobian_only_obstruction",
            node["failure_type"] == "EnclosureFailure"
            and "collision_jacobian" in node["failure_message"]
            and "relative_root" in node["failure_message"]
            and "selected_global_root" in node["failure_message"],
            node["failure_message"],
        ),
        check(
            "selector_ownership_is_nonempty",
            bool(configuration_rows),
            len(configuration_rows),
        ),
        check(
            "every_selected_configuration_is_pointwise_nonzero",
            len(pointwise_positive) == len(configuration_rows),
            f"{len(pointwise_positive)}/{len(configuration_rows)}",
        ),
        check(
            "finite_leaf_union_closes_every_selected_configuration",
            valid,
            selected_cover or "OPEN",
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_target_full_amplitude_subcuboid"]
            and not payload["valid_for_full_outer_parent_leaf_enclosure"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "collision-Jacobian leaf union only",
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
            "source_role": "collision-jacobian-leaf-union-input",
        }
        for path in source_paths()
    ]
    base_5467.atomic_csv(SOURCE_REGISTER, register)
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "selected_configuration_count",
                    "pointwise_positive_configuration_count",
                    "selected_cover",
                    "valid_for_collision_jacobian_leaf_union",
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
