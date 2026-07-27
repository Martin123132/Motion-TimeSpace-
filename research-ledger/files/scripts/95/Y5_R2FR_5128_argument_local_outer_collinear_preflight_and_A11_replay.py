from __future__ import annotations

import argparse
import cmath
import csv
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any, Callable


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5127 = (
    POST
    / "scripts"
    / "Y5_R2FR_5127_same_sheet_outer_collinear_pole_chart_and_A00_replay.py"
)
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5125"
    / "runs"
    / "reciprocal_stratified_fresh_pilot_v1"
)
CONFIG = RUN / "config.json"
SCHEDULE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5125"
    / "reciprocal_stratified_locked_schedule.json"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5128"
PREFLIGHT_JSON = SOURCE / "A11_argument_local_outer_collinear_preflight.json"
GATE_JSON = SOURCE / "A11_argument_local_outer_collinear_chart_gate.json"
CATALOG_CSV = SOURCE / "A11_argument_local_outer_collinear_catalog.csv"
RESULT_JSON = SOURCE / "A11_argument_local_outer_collinear_replay_result.json"
STATUS_JSON = SOURCE / "A11_argument_local_outer_collinear_replay_status.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5128_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5128-Y5-R2FR-argument-local-outer-collinear-preflight-and-A11-replay.md"
)

MARKER = "MTS_5128_ARGUMENT_LOCAL_OUTER_COLLINEAR_PREFLIGHT"
REVISION = "argument-local-log-cauchy-chart-v1"
CHECKED_DATE = "2026-07-20"
CHECKPOINT_ID = "5128"
JOB_KEY = "E040__S512503_N0000__A11__primary24"
EVENT_ID = "S512503_N0000"
EPSILON_ID = "E040"
BASE_ARGUMENT_ID = "A11"
INITIAL_REJECTED_GATE: Path | None = None
PRECISION_POLICY = {
    "low_boundary_nodes": 24,
    "low_global_nodes": 32,
    "low_global_residue_nodes": 48,
    "high_boundary_nodes": 32,
    "high_global_nodes": 48,
    "high_global_residue_nodes": 64,
    "acceptance_threshold_changed": False,
}
EXPECTED_COUNTS_AFTER = {
    "completed_converged": 44,
    "completed_unconverged": 0,
    "failed": 0,
    "missing": 516,
}
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5127 = load_module("mts_5127_for_5128", SCRIPT_5127)
M5126 = M5127.M5126
M5125 = M5127.M5125
M5127.JOB_KEY = JOB_KEY
M5127.MARKER = MARKER
M5127.REVISION = REVISION
M5127.CHECKED_DATE = CHECKED_DATE


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def tagged(value: dict[str, Any]) -> dict[str, Any]:
    return {
        **value,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "source_checked_date": CHECKED_DATE,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def serialize_pole(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "family": row["family"],
        "member": row["member"],
        "root": M5127.complex_row(row["root"]),
        "log_point": M5127.complex_row(row["log_point"]),
        "log_distance": row["log_distance"],
        "segment_projection": row["segment_projection"],
        "condition_residual": row["condition_residual"],
        "reciprocal_root_residual": row["reciprocal_root_residual"],
        "nearest_other_log_singularity_distance": row[
            "nearest_other_log_singularity_distance"
        ],
        "nominal_boundary_radius": row["nominal_boundary_radius"],
        "nominal_chart_radius": row["nominal_chart_radius"],
        "path_intersects_nominal_chart": row[
            "path_intersects_nominal_chart"
        ],
    }


def build_context() -> dict[str, Any]:
    config = read_json(CONFIG)
    schedule = read_json(SCHEDULE)["jobs"]
    job = next(row for row in schedule if row["job_key"] == JOB_KEY)
    manager = M5125.M5077.CentralTopologyManager(RUN, config)
    topology, topology_path, topology_runtime = manager.obtain(
        EVENT_ID, EPSILON_ID, BASE_ARGUMENT_ID
    )
    event = manager.events[EVENT_ID]
    argument = manager.arguments[f"{EPSILON_ID}_{BASE_ARGUMENT_ID}"]
    target = M5127.complex_from_row(argument["target_cosine"])
    module = M5125.M5077.M5036.N5030
    M5125.M5077.M5036.M5035.M5034.configure(event, target)
    _, ownerships = module.physical_chambers()
    if len(ownerships) != len(topology["chambers"]):
        raise RuntimeError(
            f"{CHECKPOINT_ID} physical/topological chamber count mismatch"
        )
    profile = config["tiers"]["primary24"]
    M5125.M5077.CURRENT_EVENT = event
    M5125.M5077.CURRENT_ARGUMENT = argument
    M5125.M5077.M5036.MREPAIR.CURRENT_JOB = JOB_KEY
    M5126.REPAIR_AUDIT.clear()
    chambers: list[dict[str, Any]] = []
    for chamber_index, (topology_chamber, ownership) in enumerate(
        zip(topology["chambers"], ownerships)
    ):
        start = complex(topology_chamber["target_start_log"])
        end = complex(topology_chamber["target_end_log"])
        required_roots = [
            complex(row["target_root"])
            for row in topology_chamber["surface_crossings"]
        ]
        catalog, catalog_stable = M5126.repairing_catalog(
            ownership,
            start,
            end,
            required_roots,
            int(profile["global_nodes"]),
            int(profile["global_residue_nodes"]),
            int(profile["relative_residue_nodes"]),
            float(profile["model_distance"]),
        )
        problem = {
            "event": event,
            "argument": argument,
            "module": module,
            "ownership": ownership,
            "chamber": {"residue_catalog": catalog},
            "start": start,
            "end": end,
        }
        poles = M5127.derive_outer_poles(problem)
        all_log_points = [complex(row["log_point"]) for row in catalog] + [
            complex(row["log_point"]) for row in poles
        ]
        for pole in poles:
            center = complex(pole["log_point"])
            nearest = min(
                abs(center - candidate)
                for candidate in all_log_points
                if abs(center - candidate) > 1.0e-8
            )
            nominal_boundary = M5127.BOUNDARY_FRACTION * nearest
            nominal_chart = M5127.CHART_FRACTION * nominal_boundary
            pole.update(
                {
                    "nearest_other_log_singularity_distance": float(nearest),
                    "nominal_boundary_radius": float(nominal_boundary),
                    "nominal_chart_radius": float(nominal_chart),
                    "path_intersects_nominal_chart": bool(
                        0.0 < pole["segment_projection"] < 1.0
                        and pole["log_distance"] < nominal_chart
                    ),
                }
            )
        active_poles = [
            row for row in poles if row["path_intersects_nominal_chart"]
        ]
        chambers.append(
            {
                "chamber_index": chamber_index,
                "ownership": ownership,
                "ownership_digest": M5127.ownership_digest(ownership),
                "start": start,
                "end": end,
                "catalog": catalog,
                "catalog_stable": bool(catalog_stable),
                "problem": problem,
                "poles": poles,
                "active_poles": active_poles,
            }
        )
    return {
        "config": config,
        "schedule": schedule,
        "job": job,
        "manager": manager,
        "topology": topology,
        "topology_path": Path(topology_path),
        "topology_runtime_seconds": topology_runtime,
        "event": event,
        "argument": argument,
        "target": target,
        "module": module,
        "profile": profile,
        "chambers": chambers,
    }


def structural_preflight() -> tuple[dict[str, Any], dict[str, Any]]:
    context = build_context()
    active_chambers = [
        row for row in context["chambers"] if row["active_poles"]
    ]
    active_poles = [
        pole for chamber in active_chambers for pole in chamber["active_poles"]
    ]
    checks = {
        "source_paths_exist": all(
            path.exists() for path in (SCRIPT_5127, CONFIG, SCHEDULE)
        ),
        "locked_job_selected": context["job"]
        == {
            "base_argument_id": BASE_ARGUMENT_ID,
            "epsilon_id": EPSILON_ID,
            "event_id": EVENT_ID,
            "job_key": JOB_KEY,
            "profile": "primary24",
            "seed": 512503,
            "stratum": "full_remainder",
        },
        "topology_matches_job": context["topology"]["event_id"] == EVENT_ID
        and context["topology"]["argument_id"]
        == f"{EPSILON_ID}_{BASE_ARGUMENT_ID}",
        "all_base_catalogs_stable": all(
            row["catalog_stable"] for row in context["chambers"]
        ),
        "one_argument_local_active_chamber": len(active_chambers) == 1,
        "four_active_derived_poles": len(active_poles) == 4,
        "all_active_roots_kinematic": all(
            row["condition_residual"] < M5127.ROOT_RESIDUAL_TOLERANCE
            and row["reciprocal_root_residual"]
            < M5127.ROOT_RESIDUAL_TOLERANCE
            for row in active_poles
        ),
        "locked_profile_preserved": context["profile"]
        ["relative_adaptive_tolerance"]
        == 5.0e-5
        and context["profile"]["relative_adaptive_maximum_intervals"]
        == 4096,
        "formalization_workbench_unchanged": M5127.tree_digest(FORMAL)
        == FORMAL_BASELINE,
    }
    preflight = tagged(
        {
            "job_key": JOB_KEY,
            "dry_run": True,
            "execution_authorized": all(checks.values()),
            "checks": checks,
            "topology_path": relative(context["topology_path"]),
            "topology_runtime_seconds": context["topology_runtime_seconds"],
            "target_cosine": context["argument"]["target_cosine"],
            "selection_law": (
                "activate a chart iff the target chamber segment enters the "
                "guarded disk determined before integration from the nearest "
                "known singularity"
            ),
            "chambers": [
                {
                    "chamber_index": row["chamber_index"],
                    "ownership_digest": row["ownership_digest"],
                    "start_log": str(row["start"]),
                    "end_log": str(row["end"]),
                    "base_catalog_stable": row["catalog_stable"],
                    "base_catalog_rows": len(row["catalog"]),
                    "active_pole_count": len(row["active_poles"]),
                    "poles": [serialize_pole(pole) for pole in row["poles"]],
                }
                for row in context["chambers"]
            ],
            "active_chamber_count": len(active_chambers),
            "active_pole_count": len(active_poles),
            "full_pilot_resume_authorized": False,
            "formalization_workbench_tree_sha256": M5127.tree_digest(FORMAL),
        }
    )
    atomic_json(PREFLIGHT_JSON, preflight)
    if not preflight["execution_authorized"]:
        failures = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(
            f"{CHECKPOINT_ID} structural preflight failed: {failures}"
        )
    return context, preflight


class ArgumentLocalPoleChart:
    def __init__(
        self,
        original: Callable[[complex, dict[str, bool], int, int], complex],
        chart_groups: dict[tuple[tuple[str, bool], ...], list[dict[str, Any]]],
    ) -> None:
        self.original = original
        self.chart_groups = chart_groups
        self.call_count = 0
        self.chart_call_count = 0
        self.family_counts: dict[str, int] = {}
        self.maximum_chart_fraction = 0.0

    def __call__(
        self,
        relative_circle: complex,
        ownership: dict[str, bool],
        global_nodes: int,
        global_residue_nodes: int,
    ) -> complex:
        self.call_count += 1
        charts = self.chart_groups.get(M5127.ownership_key(ownership), [])
        if (
            not charts
            or global_nodes != M5127.TARGET_GLOBAL_NODES
            or global_residue_nodes != M5127.TARGET_GLOBAL_RESIDUE_NODES
        ):
            return self.original(
                relative_circle, ownership, global_nodes, global_residue_nodes
            )
        principal_log = cmath.log(relative_circle)
        for chart in charts:
            center = complex(chart["log_point"])
            lifted = principal_log + 2.0j * math.pi * round(
                (center.imag - principal_log.imag) / (2.0 * math.pi)
            )
            displacement = lifted - center
            chart_fraction = abs(displacement) / chart["chart_radius"]
            if chart_fraction >= 1.0:
                continue
            if abs(displacement) < 1.0e-14:
                raise RuntimeError(
                    f"{CHECKPOINT_ID} true outer pole sampled exactly"
                )
            self.chart_call_count += 1
            self.family_counts[chart["family"]] = (
                self.family_counts.get(chart["family"], 0) + 1
            )
            self.maximum_chart_fraction = max(
                self.maximum_chart_fraction, chart_fraction
            )
            regular = M5127.cauchy_regular_value(
                chart["high"], displacement
            )
            return chart["high"]["residue"] / displacement + regular
        return self.original(
            relative_circle, ownership, global_nodes, global_residue_nodes
        )

    def summary(self) -> dict[str, Any]:
        return {
            "scope": JOB_KEY,
            "call_count": self.call_count,
            "chart_call_count": self.chart_call_count,
            "chart_count": sum(len(rows) for rows in self.chart_groups.values()),
            "active_ownership_count": len(self.chart_groups),
            "family_counts": dict(sorted(self.family_counts.items())),
            "maximum_chart_fraction": float(self.maximum_chart_fraction),
            "higher_precision_boundary_only": True,
            "target_global_nodes": M5127.TARGET_GLOBAL_NODES,
            "target_global_residue_nodes": M5127.TARGET_GLOBAL_RESIDUE_NODES,
        }


CATALOG_AUDIT: list[dict[str, Any]] = []


def catalog_overlay(
    chart_groups: dict[tuple[tuple[str, bool], ...], list[dict[str, Any]]]
) -> Callable[..., tuple[list[dict[str, Any]], bool]]:
    def overlay(*arguments: Any, **keywords: Any) -> tuple[list[dict[str, Any]], bool]:
        catalog, stable = M5126.repairing_catalog(*arguments, **keywords)
        ownership = arguments[0]
        start = complex(arguments[1])
        end = complex(arguments[2])
        current_job = str(M5125.M5077.M5036.MREPAIR.CURRENT_JOB)
        charts = chart_groups.get(M5127.ownership_key(ownership), [])
        if current_job != JOB_KEY or not charts:
            return catalog, stable
        for chart in charts:
            log_point, distance, projection, copy_index = M5127.nearest_log_copy(
                M5125.M5077.M5036.N5030,
                chart["root"],
                start,
                end,
            )
            center_residual = abs(log_point - chart["log_point"])
            if center_residual >= M5127.ROOT_RESIDUAL_TOLERANCE:
                raise RuntimeError(
                    f"{CHECKPOINT_ID} argument-local chart center moved by "
                    f"{center_residual}"
                )
            catalog.append(
                {
                    "root": chart["root"],
                    "pairs": [
                        [
                            f"same_sheet_outer:{chart['family']}:{chart['member']}",
                            "same_sheet_outer:derived_kinematic_denominator",
                        ]
                    ],
                    "log_point": log_point,
                    "log_distance": float(distance),
                    "segment_projection": float(projection),
                    "copy_index": int(copy_index),
                    "near_path": True,
                    "required_for_homotopy": False,
                    "outer_radius": chart["boundary_radius"],
                    "residue_method": REVISION,
                    "residue_contour_fraction": M5127.BOUNDARY_FRACTION,
                    "outer_residue": chart["low"]["residue"],
                    "inner_residue": chart["high"]["residue"],
                    "residue": chart["high"]["residue"],
                    "residue_stability": chart["residue_disagreement"],
                    "numerically_zero": False,
                    "stable": bool(chart["accepted"]),
                    "included_as_pole_model": bool(chart["accepted"]),
                    "same_sheet_outer_pole": True,
                    "pole_family": chart["family"],
                    "pole_member": chart["member"],
                }
            )
            CATALOG_AUDIT.append(
                {
                    "job_key": JOB_KEY,
                    "chamber_index": chart["chamber_index"],
                    "ownership_digest": M5127.ownership_digest(ownership),
                    "family": chart["family"],
                    "member": chart["member"],
                    "root": str(chart["root"]),
                    "log_point": str(log_point),
                    "log_distance": float(distance),
                    "segment_projection": float(projection),
                    "chart_radius": chart["chart_radius"],
                    "residue": str(chart["high"]["residue"]),
                    "residue_disagreement": chart["residue_disagreement"],
                    "double_to_simple_ratio": chart[
                        "double_to_simple_ratio"
                    ],
                    "regular_integral_uncertainty": chart[
                        "regular_integral_uncertainty"
                    ],
                    "condition_residual": chart["condition_residual"],
                    "reciprocal_root_residual": chart[
                        "reciprocal_root_residual"
                    ],
                    "accepted": bool(chart["accepted"]),
                    "included_as_pole_model": bool(chart["accepted"]),
                    "checkpoint_marker": MARKER,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                    "source_checked_date": CHECKED_DATE,
                }
            )
        return catalog, bool(stable and all(chart["accepted"] for chart in charts))

    return overlay


def build_chart_groups(
    context: dict[str, Any]
) -> tuple[
    dict[tuple[tuple[str, bool], ...], list[dict[str, Any]]], list[dict[str, Any]]
]:
    groups: dict[tuple[tuple[str, bool], ...], list[dict[str, Any]]] = {}
    all_charts: list[dict[str, Any]] = []
    for chamber in context["chambers"]:
        if not chamber["active_poles"]:
            continue
        charts = M5127.build_charts(
            chamber["problem"], chamber["active_poles"]
        )
        for chart in charts:
            chart["chamber_index"] = chamber["chamber_index"]
            chart["path_intersects_chart"] = bool(
                chart["log_distance"] < chart["chart_radius"]
                and 0.0 < chart["segment_projection"] < 1.0
            )
        groups[M5127.ownership_key(chamber["ownership"])] = charts
        all_charts.extend(charts)
    return groups, all_charts


def validation_rows(
    checks: list[tuple[str, bool, str]]
) -> list[dict[str, Any]]:
    return [
        {
            "check_id": name,
            "passed": bool(passed),
            "detail": detail,
            "checkpoint_marker": MARKER,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for name, passed, detail in checks
    ]


def build_and_write_gate(
    context: dict[str, Any], preflight: dict[str, Any]
) -> tuple[
    dict[tuple[tuple[str, bool], ...], list[dict[str, Any]]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    groups, charts = build_chart_groups(context)
    all_accepted = bool(charts) and all(chart["accepted"] for chart in charts)
    all_intersect = bool(charts) and all(
        chart["path_intersects_chart"] for chart in charts
    )
    gate = tagged(
        {
            "job_key": JOB_KEY,
            "preflight": relative(PREFLIGHT_JSON),
            "gate_accepted": bool(all_accepted and all_intersect),
            "argument_local_selection": True,
            "active_ownership_count": len(groups),
            "active_chart_count": len(charts),
            "boundary_precision_policy": PRECISION_POLICY,
            "initial_rejected_gate": (
                relative(INITIAL_REJECTED_GATE)
                if INITIAL_REJECTED_GATE is not None
                and INITIAL_REJECTED_GATE.exists()
                else None
            ),
            "all_charts_accepted": all_accepted,
            "all_target_paths_intersect_charts": all_intersect,
            "charts": [
                {
                    **M5127.serialized_chart(chart),
                    "chamber_index": chart["chamber_index"],
                    "path_intersects_chart": chart[
                        "path_intersects_chart"
                    ],
                }
                for chart in charts
            ],
            "principal_value_or_half_residue_inserted": False,
            "profile_tolerance_changed": False,
            "profile_interval_cap_changed": False,
            "seed_or_argument_changed": False,
            "full_pilot_resume_authorized": False,
            "formalization_workbench_tree_sha256": M5127.tree_digest(FORMAL),
        }
    )
    atomic_json(GATE_JSON, gate)
    return groups, charts, gate


def gate_only() -> dict[str, Any]:
    context, preflight = structural_preflight()
    _, _, gate = build_and_write_gate(context, preflight)
    return gate


def execute() -> dict[str, Any]:
    context, preflight = structural_preflight()
    groups, charts, gate = build_and_write_gate(context, preflight)
    all_accepted = bool(gate["all_charts_accepted"])
    all_intersect = bool(gate["all_target_paths_intersect_charts"])
    if not gate["gate_accepted"]:
        raise RuntimeError(
            f"{CHECKPOINT_ID} argument-local pole-chart gate rejected"
        )

    module = context["module"]
    M5125.M5077.install_history_invariant_breakpoints(module)
    previous_catalog = M5125.M5077.certified_primary_catalog
    previous_global = module.global_chamber_value
    previous_breakpoints = module.collision_scaled_breakpoints
    extension = ArgumentLocalPoleChart(previous_global, groups)
    CATALOG_AUDIT.clear()
    M5126.REPAIR_AUDIT.clear()
    M5125.M5077.certified_primary_catalog = catalog_overlay(groups)
    module.global_chamber_value = extension
    module.collision_scaled_breakpoints = M5127.chart_breakpoints(
        previous_breakpoints, charts
    )
    started = time.monotonic()
    try:
        row = M5125.execute_full_job(
            RUN,
            context["config"],
            context["manager"],
            context["job"],
        )
    finally:
        M5125.M5077.certified_primary_catalog = previous_catalog
        module.global_chamber_value = previous_global
        module.collision_scaled_breakpoints = previous_breakpoints
    replay_runtime = time.monotonic() - started

    job_path = RUN / "jobs" / f"{JOB_KEY}.json"
    kernel_path = RUN / "kernels" / f"{JOB_KEY}.json"
    kernel = read_json(kernel_path) if kernel_path.exists() else {}
    summary = extension.summary()
    profile_audit = dict(row.get("profile_audit", {}))
    profile_audit["argument_local_outer_collinear_pole_chart"] = summary
    profile_audit["argument_local_outer_collinear_catalog_rows"] = len(
        CATALOG_AUDIT
    )
    row.update(
        {
            "profile_audit": profile_audit,
            "repair_checkpoint_marker": MARKER,
            "repair_gate": relative(GATE_JSON),
            "repair_gate_sha256": M5127.digest(GATE_JSON),
        }
    )
    atomic_json(job_path, row)
    if kernel:
        kernel_profile = dict(kernel.get("profile_audit", {}))
        kernel_profile["argument_local_outer_collinear_pole_chart"] = summary
        kernel_profile["argument_local_outer_collinear_catalog_rows"] = len(
            CATALOG_AUDIT
        )
        kernel.update(
            {
                "profile_audit": kernel_profile,
                "repair_checkpoint_marker": MARKER,
                "repair_gate": relative(GATE_JSON),
                "repair_gate_sha256": M5127.digest(GATE_JSON),
            }
        )
        atomic_json(kernel_path, kernel)
    write_csv(CATALOG_CSV, CATALOG_AUDIT)

    fixed_gate = kernel.get("fixed_event_integral_gate", {})
    order_rows = fixed_gate.get("order_rows", [])
    highest = order_rows[-1] if order_rows else {}
    counts = M5125.run_counts(
        RUN, context["config"]["config_digest"], context["schedule"]
    )
    state = (
        f"PAUSED_AFTER_{CHECKPOINT_ID}_{BASE_ARGUMENT_ID}_REPLAY"
        if row.get("status") == "COMPLETED_CONVERGED"
        else f"BLOCKED_{CHECKPOINT_ID}_{BASE_ARGUMENT_ID}_REPLAY"
    )
    status = tagged(
        {
            "state": state,
            "run_id": RUN.name,
            "job_key": JOB_KEY,
            "job_status": row.get("status"),
            "replay_runtime_seconds": replay_runtime,
            "expected_job_count": len(context["schedule"]),
            **counts,
            "chart_summary": summary,
            "catalog_row_count": len(CATALOG_AUDIT),
            "full_pilot_resume_authorized": False,
            "formalization_unchanged": M5127.tree_digest(FORMAL)
            == FORMAL_BASELINE,
        }
    )
    atomic_json(STATUS_JSON, status)
    atomic_json(RUN / "status.json", status)
    result = tagged(
        {
            "job_key": JOB_KEY,
            "preflight": relative(PREFLIGHT_JSON),
            "gate": relative(GATE_JSON),
            "catalog": relative(CATALOG_CSV),
            "job_status": row.get("status"),
            "integral_converged": bool(row.get("integral_converged")),
            "composite_interval_count": highest.get(
                "composite_interval_count"
            ),
            "maximum_adaptive_chamber_relative_error": highest.get(
                "maximum_adaptive_chamber_relative_error"
            ),
            "causally_corrected_value": highest.get(
                "causally_corrected_value"
            ),
            "normalized_direct_D_hhh_over_G3": row.get(
                "normalized_direct_D_hhh_over_G3"
            ),
            "chart_summary": summary,
            "catalog_rows": CATALOG_AUDIT,
            "boundary_precision_policy": PRECISION_POLICY,
            "initial_rejected_gate": gate["initial_rejected_gate"],
            "run_counts": counts,
            "profile_tolerance": context["profile"]
            ["relative_adaptive_tolerance"],
            "profile_interval_cap": context["profile"]
            ["relative_adaptive_maximum_intervals"],
            "formalization_workbench_tree_sha256": M5127.tree_digest(FORMAL),
            "interpretation": (
                f"The same event-level pole law is selected by the "
                f"{BASE_ARGUMENT_ID} contour "
                "geometry without a retuned threshold or altered field equation. "
                "This remains a numerical pipeline result, not an MTS claim."
            ),
        }
    )
    atomic_json(RESULT_JSON, result)

    tolerance = float(context["profile"]["relative_adaptive_tolerance"])
    error = float(
        highest.get("maximum_adaptive_chamber_relative_error", math.inf)
    )
    checks = [
        (
            "source_paths_exist",
            all(
                path.exists()
                for path in (
                    SCRIPT_5127,
                    PREFLIGHT_JSON,
                    GATE_JSON,
                    CATALOG_CSV,
                    job_path,
                    kernel_path,
                )
            ),
            f"all {CHECKPOINT_ID} source and live witness paths exist",
        ),
        (
            "argument_local_preflight_passed",
            bool(preflight["execution_authorized"]),
            str(preflight["active_chamber_count"]),
        ),
        (
            "four_charts_accepted",
            len(charts) == 4 and all_accepted,
            str(len(charts)),
        ),
        (
            "all_charts_intersect_target_path",
            all_intersect,
            str([chart["log_distance"] for chart in charts]),
        ),
        (
            "all_four_models_inserted",
            len(CATALOG_AUDIT) == 4
            and all(row["included_as_pole_model"] for row in CATALOG_AUDIT),
            str(len(CATALOG_AUDIT)),
        ),
        (
            "chart_route_exercised",
            extension.chart_call_count > 0,
            str(extension.chart_call_count),
        ),
        (
            f"{BASE_ARGUMENT_ID}_replay_converged",
            row.get("status") == "COMPLETED_CONVERGED"
            and row.get("strict_adaptive_validated") is True
            and bool(fixed_gate.get("fixed_event_crossed_integral_converged"))
            and bool(fixed_gate.get("strict_adaptive_quadrature_converged")),
            str(row.get("status")),
        ),
        (
            "adaptive_error_below_unchanged_tolerance",
            error <= tolerance,
            f"error={error};tolerance={tolerance}",
        ),
        (
            "locked_profile_preserved",
            result["profile_tolerance"] == 5.0e-5
            and result["profile_interval_cap"] == 4096,
            f"tol={result['profile_tolerance']};cap={result['profile_interval_cap']}",
        ),
        (
            "single_job_only",
            counts == EXPECTED_COUNTS_AFTER,
            str(counts),
        ),
        (
            "formalization_workbench_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_numeric_UV_claim"]
            and not result["valid_for_local_GR_claim"]
            and not result["valid_for_full_MTS_claim"],
            "pipeline result only",
        ),
    ]
    write_csv(VALIDATION_CSV, validation_rows(checks))
    failures = [name for name, passed, _ in checks if not passed]
    write_document(result, failures)
    if failures:
        raise RuntimeError(
            f"{CHECKPOINT_ID} validation failed: {failures}"
        )
    return result


def finalize_existing() -> dict[str, Any]:
    if not RESULT_JSON.exists():
        raise RuntimeError(
            f"{CHECKPOINT_ID} cannot finalize a missing replay result"
        )
    result = read_json(RESULT_JSON)
    preflight = read_json(PREFLIGHT_JSON)
    gate = read_json(GATE_JSON)
    job_path = RUN / "jobs" / f"{JOB_KEY}.json"
    kernel_path = RUN / "kernels" / f"{JOB_KEY}.json"
    job = read_json(job_path)
    kernel = read_json(kernel_path)
    fixed_gate = kernel["fixed_event_integral_gate"]
    catalog_rows = result["catalog_rows"]
    counts = result["run_counts"]
    error = float(result["maximum_adaptive_chamber_relative_error"])
    tolerance = float(result["profile_tolerance"])
    checks = [
        (
            "source_paths_exist",
            all(
                path.exists()
                for path in (
                    SCRIPT_5127,
                    PREFLIGHT_JSON,
                    GATE_JSON,
                    CATALOG_CSV,
                    job_path,
                    kernel_path,
                )
            ),
            f"all {CHECKPOINT_ID} source and live witness paths exist",
        ),
        (
            "argument_local_preflight_passed",
            bool(preflight["execution_authorized"]),
            str(preflight["active_chamber_count"]),
        ),
        (
            "four_charts_accepted",
            int(gate["active_chart_count"]) == 4
            and bool(gate["all_charts_accepted"]),
            str(gate["active_chart_count"]),
        ),
        (
            "all_charts_intersect_target_path",
            bool(gate["all_target_paths_intersect_charts"]),
            str([row["log_distance"] for row in gate["charts"]]),
        ),
        (
            "all_four_models_inserted",
            len(catalog_rows) == 4
            and all(row["included_as_pole_model"] for row in catalog_rows),
            str(len(catalog_rows)),
        ),
        (
            "chart_route_exercised",
            int(result["chart_summary"]["chart_call_count"]) > 0,
            str(result["chart_summary"]["chart_call_count"]),
        ),
        (
            f"{BASE_ARGUMENT_ID}_replay_converged",
            job.get("status") == "COMPLETED_CONVERGED"
            and job.get("strict_adaptive_validated") is True
            and bool(result["integral_converged"])
            and bool(fixed_gate["fixed_event_crossed_integral_converged"])
            and bool(fixed_gate["strict_adaptive_quadrature_converged"]),
            str(job.get("status")),
        ),
        (
            "adaptive_error_below_unchanged_tolerance",
            error <= tolerance,
            f"error={error};tolerance={tolerance}",
        ),
        (
            "locked_profile_preserved",
            tolerance == 5.0e-5
            and int(result["profile_interval_cap"]) == 4096,
            f"tol={tolerance};cap={result['profile_interval_cap']}",
        ),
        (
            "single_job_only",
            counts == EXPECTED_COUNTS_AFTER,
            str(counts),
        ),
        (
            "formalization_workbench_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_numeric_UV_claim"]
            and not result["valid_for_local_GR_claim"]
            and not result["valid_for_full_MTS_claim"],
            "pipeline result only",
        ),
    ]
    write_csv(VALIDATION_CSV, validation_rows(checks))
    failures = [name for name, passed, _ in checks if not passed]
    write_document(result, failures)
    if failures:
        raise RuntimeError(
            f"{CHECKPOINT_ID} existing-result validation failed: {failures}"
        )
    return result


def write_document(result: dict[str, Any], failures: list[str]) -> None:
    status = result["job_status"]
    preflight = read_json(PREFLIGHT_JSON)
    chamber_summary = ", ".join(
        f"chamber {row['chamber_index']}: {row['active_pole_count']}"
        for row in preflight["chambers"]
    )
    precision = result["boundary_precision_policy"]
    text = f"""# {CHECKPOINT_ID} - argument-local outer-collinear preflight and {BASE_ARGUMENT_ID} replay

## Result

Checkpoint 5127's pole equations are event-level laws, while proximity to an
integration chamber is argument-local geometry. The locked
`{BASE_ARGUMENT_ID}` preflight therefore derives the roots first and activates
no chart unless the target contour enters its isolation disk. The resulting
selection is `{chamber_summary}`. No numerical outcome was used to select it.

The exact locked job `{JOB_KEY}` ends as `{status}`. It uses
`{result['composite_interval_count']}` composite intervals and reaches maximum
adaptive relative error `{result['maximum_adaptive_chamber_relative_error']}`
against the unchanged `5e-5` tolerance. The causally corrected value is
`{result['causally_corrected_value']}`.

The chart was called `{result['chart_summary']['chart_call_count']}` times
inside `{result['chart_summary']['call_count']}` target-profile evaluations.
Its low/high boundary levels are
`{precision['low_boundary_nodes']}/{precision['low_global_nodes']}/{precision['low_global_residue_nodes']}`
and
`{precision['high_boundary_nodes']}/{precision['high_global_nodes']}/{precision['high_global_residue_nodes']}`;
the acceptance threshold was not changed.
The durable pilot count is
`{result['run_counts']['completed_converged']}/560` converged,
`{result['run_counts']['completed_unconverged']}` unconverged,
`{result['run_counts']['failed']}` failed and
`{result['run_counts']['missing']}` missing.

## Cog interpretation

This is the numerical analogue of the machine/cog requirement: one derived
pole law is retained, but the contour geometry decides whether it is active.
There is no hand-set argument switch and no tolerance retuning. This does not
yet establish the physical MTS transition between local GR and galaxies; it
does establish the required discipline in the coefficient pipeline.

## Discipline

- Validation failures: `{failures}`.
- Full-pilot continuation remains unauthorized.
- No principal value or half residue was inserted.
- The protected formalization tree remains `{FORMAL_BASELINE}`.
- No UV coefficient, local-GR, galaxy, or full-MTS claim follows.
- No GitHub action occurred.

## Next

Run the next untouched argument only after applying this preflight to its
transported contour. Do not infer that all later arguments share
`{BASE_ARGUMENT_ID}`'s active
chamber and do not bulk-resume the schedule.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "gate", "execute", "finalize-existing"),
        default="dry-run",
    )
    arguments = parser.parse_args()
    if arguments.mode == "dry-run":
        _, result = structural_preflight()
    elif arguments.mode == "gate":
        result = gate_only()
    elif arguments.mode == "finalize-existing":
        result = finalize_existing()
    else:
        result = execute()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
