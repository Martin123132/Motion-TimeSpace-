from __future__ import annotations

import argparse
import cmath
import csv
import hashlib
import importlib.util
import json
import math
import os
import shutil
import time
from pathlib import Path
from typing import Any, Callable


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5126 = (
    POST
    / "scripts"
    / "Y5_R2FR_5126_reciprocal_partner_residue_repair_and_pilot_resume.py"
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
SOURCE = POST / "source-intake" / "functional_rg" / "5127"
WITNESS_JOB = RUN / "jobs" / "E040__S512503_N0000__A00__primary24.json"
WITNESS_KERNEL = (
    RUN / "kernels" / "E040__S512503_N0000__A00__primary24.json"
)
ORIGINAL_JOB = SOURCE / "A00_original_unconverged_job.json"
ORIGINAL_KERNEL = SOURCE / "A00_original_unconverged_kernel.json"
DRY_RUN_JSON = SOURCE / "same_sheet_outer_collinear_structural_dry_run.json"
GATE_JSON = SOURCE / "same_sheet_outer_collinear_pole_chart_gate.json"
CATALOG_CSV = SOURCE / "same_sheet_outer_collinear_pole_catalog.csv"
RESULT_JSON = SOURCE / "A00_outer_collinear_pole_chart_replay_result.json"
STATUS_JSON = SOURCE / "A00_outer_collinear_pole_chart_replay_status.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5127_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5127-Y5-R2FR-same-sheet-outer-collinear-pole-chart-and-A00-replay.md"
)

MARKER = "MTS_5127_SAME_SHEET_OUTER_COLLINEAR_POLE_CHART"
REVISION = "derived-outer-collinear-log-cauchy-chart-v1"
CHECKED_DATE = "2026-07-19"
JOB_KEY = "E040__S512503_N0000__A00__primary24"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

BOUNDARY_FRACTION = 0.12
CHART_FRACTION = 0.65
HIGH_BOUNDARY_NODES = 32
HIGH_GLOBAL_NODES = 48
HIGH_RESIDUE_NODES = 64
LOW_BOUNDARY_NODES = 24
LOW_GLOBAL_NODES = 32
LOW_RESIDUE_NODES = 48
MAXIMUM_RESIDUE_DISAGREEMENT = 5.0e-5
MAXIMUM_DOUBLE_TO_SIMPLE_RATIO = 2.0e-4
MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY = 2.0e-4
ROOT_RESIDUAL_TOLERANCE = 2.0e-12
TARGET_CHAMBER_INDEX = 1
TARGET_GLOBAL_NODES = 24
TARGET_GLOBAL_RESIDUE_NODES = 24


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5126 = load_module("mts_5126_for_5127", SCRIPT_5126)
M5125 = M5126.M5125


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def complex_from_row(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


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


def ownership_key(ownership: dict[str, bool]) -> tuple[tuple[str, bool], ...]:
    return tuple(sorted((key, bool(value)) for key, value in ownership.items()))


def ownership_digest(ownership: dict[str, bool]) -> str:
    payload = json.dumps(dict(ownership_key(ownership)), sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def preserve_original_witness() -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    if not ORIGINAL_JOB.exists():
        current = read_json(WITNESS_JOB)
        if current.get("status") != "COMPLETED_UNCONVERGED":
            raise RuntimeError(
                "5127 cannot preserve the original A00 witness because the live row "
                f"has status {current.get('status')}"
            )
        shutil.copy2(WITNESS_JOB, ORIGINAL_JOB)
    if not ORIGINAL_KERNEL.exists():
        current = read_json(WITNESS_KERNEL)
        if current["fixed_event_integral_gate"][
            "fixed_event_crossed_integral_converged"
        ]:
            raise RuntimeError("5127 original A00 kernel is already converged")
        shutil.copy2(WITNESS_KERNEL, ORIGINAL_KERNEL)


def configured_problem() -> dict[str, Any]:
    preserve_original_witness()
    job = read_json(ORIGINAL_JOB)
    kernel = read_json(ORIGINAL_KERNEL)
    if job["job_key"] != JOB_KEY or kernel["job_key"] != JOB_KEY:
        raise RuntimeError("5127 witness job key changed")
    event = kernel["event"]
    argument = kernel["argument"]
    target = complex_from_row(argument["target_cosine"])
    module = M5125.M5077.M5036.N5030
    M5125.M5077.M5036.M5035.M5034.configure(event, target)
    _, ownerships = module.physical_chambers()
    chamber = kernel["fixed_event_integral_gate"]["chambers"][
        TARGET_CHAMBER_INDEX
    ]
    return {
        "job": job,
        "kernel": kernel,
        "event": event,
        "argument": argument,
        "target": target,
        "module": module,
        "ownership": ownerships[TARGET_CHAMBER_INDEX],
        "chamber": chamber,
        "start": complex(chamber["start_log"]),
        "end": complex(chamber["end_log"]),
    }


def reciprocal_roots_from_cosine(
    soft_cosine: float, decay_cosine: float, relative_cosine: complex
) -> tuple[complex, complex]:
    soft_transverse = math.sqrt(max(0.0, 1.0 - soft_cosine * soft_cosine))
    decay_transverse = math.sqrt(max(0.0, 1.0 - decay_cosine * decay_cosine))
    transverse_product = soft_transverse * decay_transverse
    if transverse_product <= 0.0:
        raise RuntimeError("degenerate relative-azimuth transverse product")
    coefficient = (
        2.0 * (relative_cosine - soft_cosine * decay_cosine)
        / transverse_product
    )
    discriminant = cmath.sqrt(coefficient * coefficient - 4.0)
    first = (coefficient + discriminant) / 2.0
    second = (coefficient - discriminant) / 2.0
    return first, second


def nearest_log_copy(
    module: Any, root: complex, start: complex, end: complex
) -> tuple[complex, float, float, int]:
    return module.nearest_log_copy_to_segment(root, start, end)


def derive_outer_poles(problem: dict[str, Any]) -> list[dict[str, Any]]:
    event = problem["event"]
    module = problem["module"]
    start = problem["start"]
    end = problem["end"]
    kinematics = module.M5028.M5027
    beam_first, beam_second, beam_cosine = kinematics.relative_azimuth_roots(
        float(event["soft_energy"]),
        float(event["soft_cosine"]),
        float(event["decay_cosine"]),
        1.0,
        1.0,
    )
    beam_roots = sorted((complex(beam_first), complex(beam_second)), key=abs)
    soft_roots = sorted(
        reciprocal_roots_from_cosine(
            float(event["soft_cosine"]),
            float(event["decay_cosine"]),
            1.0 + 0.0j,
        ),
        key=abs,
    )
    definitions = [
        (
            "beam_spinor",
            beam_roots,
            complex(beam_cosine),
            "p_1^- = E_1-p_{1z}=0",
        ),
        (
            "hard_soft_invariant",
            soft_roots,
            1.0 + 0.0j,
            "s_13=2 e A (1+beta) (1-C)=0",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for family, roots, relative_cosine, equation in definitions:
        reciprocal_residual = abs(roots[0] * roots[1] - 1.0)
        for member, root in zip(("small", "large"), roots):
            log_point, distance, projection, copy_index = nearest_log_copy(
                module, root, start, end
            )
            soft_direction, decay_direction, internal = module.M5028.event_geometry(
                float(event["soft_energy"]),
                complex(float(event["soft_cosine"]), 0.0),
                complex(float(event["decay_cosine"]), 0.0),
                root,
            )
            if family == "beam_spinor":
                condition_value = complex(internal[0, 0] - internal[0, 3])
                condition_scale = max(
                    1.0,
                    abs(complex(internal[0, 0])),
                    abs(complex(internal[0, 3])),
                )
            else:
                first = internal[0]
                third = internal[2]
                condition_value = 2.0 * (
                    first[0] * third[0]
                    - sum(first[index] * third[index] for index in range(1, 4))
                )
                condition_scale = max(
                    1.0,
                    abs(complex(first[0] * third[0])),
                )
            rows.append(
                {
                    "family": family,
                    "member": member,
                    "root": root,
                    "log_point": log_point,
                    "log_distance": float(distance),
                    "segment_projection": float(projection),
                    "copy_index": int(copy_index),
                    "relative_cosine": relative_cosine,
                    "equation": equation,
                    "condition_residual": float(
                        abs(condition_value) / condition_scale
                    ),
                    "reciprocal_root_residual": float(reciprocal_residual),
                }
            )
    rows.sort(key=lambda row: row["segment_projection"])
    return rows


def cauchy_boundary(
    original: Callable[[complex, dict[str, bool], int, int], complex],
    ownership: dict[str, bool],
    center: complex,
    radius: float,
    boundary_nodes: int,
    global_nodes: int,
    residue_nodes: int,
) -> dict[str, Any]:
    phases = [
        cmath.exp(2.0j * math.pi * (index + 0.317) / boundary_nodes)
        for index in range(boundary_nodes)
    ]
    started = time.monotonic()
    values = [
        original(
            cmath.exp(center + radius * phase),
            ownership,
            global_nodes,
            residue_nodes,
        )
        for phase in phases
    ]
    residue = sum(
        value * radius * phase for value, phase in zip(values, phases)
    ) / boundary_nodes
    second_principal = sum(
        value * (radius * phase) ** 2
        for value, phase in zip(values, phases)
    ) / boundary_nodes
    regular_values = [
        value - residue / (radius * phase)
        for value, phase in zip(values, phases)
    ]
    return {
        "boundary_nodes": boundary_nodes,
        "global_nodes": global_nodes,
        "global_residue_nodes": residue_nodes,
        "radius": radius,
        "phases": phases,
        "values": values,
        "regular_values": regular_values,
        "residue": residue,
        "second_principal_coefficient": second_principal,
        "runtime_seconds": time.monotonic() - started,
    }


def cauchy_regular_value(boundary: dict[str, Any], displacement: complex) -> complex:
    radius = float(boundary["radius"])
    return sum(
        value * (radius * phase) / (radius * phase - displacement)
        for value, phase in zip(
            boundary["regular_values"], boundary["phases"]
        )
    ) / len(boundary["phases"])


def serialized_boundary(boundary: dict[str, Any]) -> dict[str, Any]:
    return {
        "boundary_nodes": int(boundary["boundary_nodes"]),
        "global_nodes": int(boundary["global_nodes"]),
        "global_residue_nodes": int(boundary["global_residue_nodes"]),
        "radius": float(boundary["radius"]),
        "residue": complex_row(boundary["residue"]),
        "second_principal_coefficient": complex_row(
            boundary["second_principal_coefficient"]
        ),
        "runtime_seconds": float(boundary["runtime_seconds"]),
        "samples": [
            {
                "phase": complex_row(phase),
                "value": complex_row(value),
                "regular_value": complex_row(regular),
            }
            for phase, value, regular in zip(
                boundary["phases"],
                boundary["values"],
                boundary["regular_values"],
            )
        ],
    }


def build_charts(
    problem: dict[str, Any], pole_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    module = problem["module"]
    ownership = problem["ownership"]
    original = module.global_chamber_value
    base_log_points = [
        complex(row["log_point"])
        for row in problem["chamber"]["residue_catalog"]
    ]
    all_log_points = base_log_points + [row["log_point"] for row in pole_rows]
    charts: list[dict[str, Any]] = []
    for row in pole_rows:
        center = complex(row["log_point"])
        nearest_distance = min(
            abs(center - candidate)
            for candidate in all_log_points
            if abs(center - candidate) > 1.0e-8
        )
        radius = BOUNDARY_FRACTION * nearest_distance
        chart_radius = CHART_FRACTION * radius
        high = cauchy_boundary(
            original,
            ownership,
            center,
            radius,
            HIGH_BOUNDARY_NODES,
            HIGH_GLOBAL_NODES,
            HIGH_RESIDUE_NODES,
        )
        low = cauchy_boundary(
            original,
            ownership,
            center,
            radius,
            LOW_BOUNDARY_NODES,
            LOW_GLOBAL_NODES,
            LOW_RESIDUE_NODES,
        )
        residue_disagreement = abs(high["residue"] - low["residue"]) / max(
            1.0, abs(high["residue"]), abs(low["residue"])
        )
        double_to_simple_ratio = abs(high["second_principal_coefficient"]) / max(
            abs(high["residue"]) * radius, 1.0e-30
        )
        probes = [0.0j]
        for fraction in (0.25, 0.50):
            for direction in (1.0 + 0.0j, 1.0j, -1.0 + 0.0j, -1.0j):
                probes.append(fraction * chart_radius * direction)
        probe_rows: list[dict[str, Any]] = []
        maximum_regular_difference = 0.0
        for displacement in probes:
            high_value = cauchy_regular_value(high, displacement)
            low_value = cauchy_regular_value(low, displacement)
            difference = abs(high_value - low_value)
            maximum_regular_difference = max(maximum_regular_difference, difference)
            probe_rows.append(
                {
                    "displacement": complex_row(displacement),
                    "high_regular_value": complex_row(high_value),
                    "low_regular_value": complex_row(low_value),
                    "absolute_difference": float(difference),
                }
            )
        regular_integral_uncertainty = (
            maximum_regular_difference * 2.0 * chart_radius / (2.0 * math.pi)
        )
        accepted = bool(
            row["condition_residual"] < ROOT_RESIDUAL_TOLERANCE
            and row["reciprocal_root_residual"] < ROOT_RESIDUAL_TOLERANCE
            and residue_disagreement < MAXIMUM_RESIDUE_DISAGREEMENT
            and double_to_simple_ratio < MAXIMUM_DOUBLE_TO_SIMPLE_RATIO
            and regular_integral_uncertainty
            < MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY
        )
        charts.append(
            {
                **row,
                "nearest_other_log_singularity_distance": float(nearest_distance),
                "boundary_radius": float(radius),
                "chart_radius": float(chart_radius),
                "high": high,
                "low": low,
                "residue_disagreement": float(residue_disagreement),
                "double_to_simple_ratio": float(double_to_simple_ratio),
                "maximum_regular_difference": float(maximum_regular_difference),
                "regular_integral_uncertainty": float(
                    regular_integral_uncertainty
                ),
                "probe_rows": probe_rows,
                "accepted": accepted,
            }
        )
    for first_index, first in enumerate(charts):
        for second in charts[first_index + 1 :]:
            if abs(first["log_point"] - second["log_point"]) <= (
                first["chart_radius"] + second["chart_radius"]
            ):
                raise RuntimeError(
                    "5127 outer-collinear Cauchy charts overlap: "
                    f"{first['family']}:{first['member']} and "
                    f"{second['family']}:{second['member']}"
                )
    return charts


def serialized_chart(chart: dict[str, Any]) -> dict[str, Any]:
    return {
        "family": chart["family"],
        "member": chart["member"],
        "root": complex_row(chart["root"]),
        "log_point": complex_row(chart["log_point"]),
        "log_distance": chart["log_distance"],
        "segment_projection": chart["segment_projection"],
        "relative_cosine": complex_row(chart["relative_cosine"]),
        "equation": chart["equation"],
        "condition_residual": chart["condition_residual"],
        "reciprocal_root_residual": chart["reciprocal_root_residual"],
        "nearest_other_log_singularity_distance": chart[
            "nearest_other_log_singularity_distance"
        ],
        "boundary_radius": chart["boundary_radius"],
        "chart_radius": chart["chart_radius"],
        "high_boundary": serialized_boundary(chart["high"]),
        "low_boundary": serialized_boundary(chart["low"]),
        "residue_disagreement": chart["residue_disagreement"],
        "double_to_simple_ratio": chart["double_to_simple_ratio"],
        "maximum_regular_difference": chart["maximum_regular_difference"],
        "regular_integral_uncertainty": chart[
            "regular_integral_uncertainty"
        ],
        "probe_rows": chart["probe_rows"],
        "accepted": chart["accepted"],
    }


class CertifiedOuterCollinearPoleChart:
    def __init__(
        self,
        original: Callable[[complex, dict[str, bool], int, int], complex],
        ownership: dict[str, bool],
        charts: list[dict[str, Any]],
    ) -> None:
        self.original = original
        self.ownership = ownership_key(ownership)
        self.charts = charts
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
        if (
            ownership_key(ownership) != self.ownership
            or global_nodes != TARGET_GLOBAL_NODES
            or global_residue_nodes != TARGET_GLOBAL_RESIDUE_NODES
        ):
            return self.original(
                relative_circle, ownership, global_nodes, global_residue_nodes
            )
        principal_log = cmath.log(relative_circle)
        for chart in self.charts:
            center = complex(chart["log_point"])
            lifted = principal_log + 2.0j * math.pi * round(
                (center.imag - principal_log.imag) / (2.0 * math.pi)
            )
            displacement = lifted - center
            chart_fraction = abs(displacement) / chart["chart_radius"]
            if chart_fraction >= 1.0:
                continue
            if abs(displacement) < 1.0e-14:
                raise RuntimeError("5127 true outer pole sampled exactly")
            self.chart_call_count += 1
            self.family_counts[chart["family"]] = (
                self.family_counts.get(chart["family"], 0) + 1
            )
            self.maximum_chart_fraction = max(
                self.maximum_chart_fraction, chart_fraction
            )
            regular = cauchy_regular_value(chart["high"], displacement)
            return chart["high"]["residue"] / displacement + regular
        return self.original(
            relative_circle, ownership, global_nodes, global_residue_nodes
        )

    def summary(self) -> dict[str, Any]:
        return {
            "call_count": self.call_count,
            "chart_call_count": self.chart_call_count,
            "family_counts": dict(sorted(self.family_counts.items())),
            "maximum_chart_fraction": float(self.maximum_chart_fraction),
            "chart_count": len(self.charts),
            "scope": JOB_KEY,
            "higher_precision_boundary_only": True,
            "target_global_nodes": TARGET_GLOBAL_NODES,
            "target_global_residue_nodes": TARGET_GLOBAL_RESIDUE_NODES,
        }


CATALOG_AUDIT: list[dict[str, Any]] = []


def catalog_overlay(
    charts: list[dict[str, Any]],
    target_ownership: dict[str, bool],
) -> Callable[..., tuple[list[dict[str, Any]], bool]]:
    target_key = ownership_key(target_ownership)

    def overlay(*arguments: Any, **keywords: Any) -> tuple[list[dict[str, Any]], bool]:
        catalog, stable = M5126.repairing_catalog(*arguments, **keywords)
        ownership = arguments[0]
        start = complex(arguments[1])
        end = complex(arguments[2])
        current_job = str(M5125.M5077.M5036.MREPAIR.CURRENT_JOB)
        if current_job != JOB_KEY or ownership_key(ownership) != target_key:
            return catalog, stable
        for chart in charts:
            log_point, distance, projection, copy_index = nearest_log_copy(
                M5125.M5077.M5036.N5030,
                chart["root"],
                start,
                end,
            )
            center_residual = abs(log_point - chart["log_point"])
            if center_residual >= ROOT_RESIDUAL_TOLERANCE:
                raise RuntimeError(
                    f"5127 chart center moved by {center_residual}"
                )
            row = {
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
                "residue_contour_fraction": BOUNDARY_FRACTION,
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
            catalog.append(row)
            CATALOG_AUDIT.append(
                {
                    "job_key": JOB_KEY,
                    "family": chart["family"],
                    "member": chart["member"],
                    "root": str(chart["root"]),
                    "log_point": str(log_point),
                    "log_distance": float(distance),
                    "segment_projection": float(projection),
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


def chart_breakpoints(
    original: Callable[[complex, complex, list[dict[str, Any]]], list[float]],
    charts: list[dict[str, Any]],
) -> Callable[[complex, complex, list[dict[str, Any]]], list[float]]:
    def breakpoints(
        start: complex, end: complex, catalog: list[dict[str, Any]]
    ) -> list[float]:
        points = list(original(start, end, catalog))
        difference = end - start
        quadratic = abs(difference) ** 2
        for chart in charts:
            relative_start = start - chart["log_point"]
            linear = 2.0 * (relative_start * difference.conjugate()).real
            constant = abs(relative_start) ** 2 - chart["chart_radius"] ** 2
            discriminant = linear * linear - 4.0 * quadratic * constant
            if discriminant < 0.0:
                continue
            root = math.sqrt(discriminant)
            for point in (
                (-linear - root) / (2.0 * quadratic),
                (-linear + root) / (2.0 * quadratic),
            ):
                if 0.0 < point < 1.0:
                    points.append(float(point))
        return sorted({round(float(point), 12) for point in points})

    breakpoints._mts_outer_collinear_chart = True  # type: ignore[attr-defined]
    return breakpoints


def structural_dry_run() -> dict[str, Any]:
    problem = configured_problem()
    poles = derive_outer_poles(problem)
    config = read_json(CONFIG)
    checks = {
        "source_paths_exist": all(
            path.exists()
            for path in (
                SCRIPT_5126,
                CONFIG,
                SCHEDULE,
                ORIGINAL_JOB,
                ORIGINAL_KERNEL,
            )
        ),
        "locked_witness_is_A00": problem["job"]["job_key"] == JOB_KEY,
        "locked_witness_is_unconverged": problem["job"]["status"]
        == "COMPLETED_UNCONVERGED",
        "locked_config_digest_preserved": problem["job"]["config_digest"]
        == config["config_digest"],
        "four_outer_roots_derived": len(poles) == 4,
        "two_reciprocal_families": all(
            row["reciprocal_root_residual"] < ROOT_RESIDUAL_TOLERANCE
            for row in poles
        ),
        "kinematic_conditions_close": all(
            row["condition_residual"] < ROOT_RESIDUAL_TOLERANCE for row in poles
        ),
        "all_roots_are_near_target_chamber": all(
            row["log_distance"] < 3.0e-4
            and 0.0 < row["segment_projection"] < 1.0
            for row in poles
        ),
        "profile_thresholds_unchanged": config["tiers"]["primary24"]
        ["relative_adaptive_tolerance"]
        == 5.0e-5
        and config["tiers"]["primary24"]
        ["relative_adaptive_maximum_intervals"]
        == 4096,
        "formalization_workbench_unchanged": tree_digest(FORMAL)
        == FORMAL_BASELINE,
    }
    result = tagged(
        {
            "dry_run": True,
            "execution_authorized": all(checks.values()),
            "checks": checks,
            "derived_poles": [
                {
                    **{
                        key: value
                        for key, value in row.items()
                        if key not in {"root", "log_point", "relative_cosine"}
                    },
                    "root": complex_row(row["root"]),
                    "log_point": complex_row(row["log_point"]),
                    "relative_cosine": complex_row(row["relative_cosine"]),
                }
                for row in poles
            ],
            "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        }
    )
    atomic_json(DRY_RUN_JSON, result)
    if not result["execution_authorized"]:
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"5127 structural dry-run failed: {failed}")
    return result


def validation_rows(
    checks: list[tuple[str, bool, str]]
) -> list[dict[str, Any]]:
    return [
        {
            "check_id": check_id,
            "passed": bool(passed),
            "detail": detail,
            "checkpoint_marker": MARKER,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for check_id, passed, detail in checks
    ]


def execute() -> dict[str, Any]:
    dry = structural_dry_run()
    if not dry["execution_authorized"]:
        raise RuntimeError("5127 dry-run did not authorize execution")
    problem = configured_problem()
    poles = derive_outer_poles(problem)
    charts = build_charts(problem, poles)
    all_charts_accepted = all(chart["accepted"] for chart in charts)
    gate = tagged(
        {
            "job_key": JOB_KEY,
            "gate_accepted": all_charts_accepted,
            "derivation": {
                "relative_cosine": (
                    "C(q)=c_s c_d+s_s s_d(q+q^-1)/2"
                ),
                "beam_spinor_family": (
                    "p_1^-=E_1-p_1z is affine in C; p_1^-=0 gives "
                    "C=C_beam and a reciprocal quadratic in q"
                ),
                "hard_soft_family": (
                    "s_13=2 e A(1+beta)(1-C); s_13=0 gives C=1 "
                    "and a reciprocal quadratic in q"
                ),
                "log_form": (
                    "F(z)=R/(z-z0)+H(z), with H reconstructed by the "
                    "Cauchy formula from an isolated boundary"
                ),
                "integration": (
                    "subtract R/(z-z0), integrate it analytically, and use "
                    "the certified Cauchy chart only inside its guarded disk"
                ),
            },
            "thresholds": {
                "boundary_fraction": BOUNDARY_FRACTION,
                "chart_fraction": CHART_FRACTION,
                "maximum_residue_disagreement": MAXIMUM_RESIDUE_DISAGREEMENT,
                "maximum_double_to_simple_ratio": MAXIMUM_DOUBLE_TO_SIMPLE_RATIO,
                "maximum_regular_integral_uncertainty": (
                    MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY
                ),
                "root_residual_tolerance": ROOT_RESIDUAL_TOLERANCE,
            },
            "charts": [serialized_chart(chart) for chart in charts],
            "all_charts_isolated": True,
            "all_charts_accepted": all_charts_accepted,
            "principal_value_or_half_residue_inserted": False,
            "profile_tolerance_changed": False,
            "profile_interval_cap_changed": False,
            "seed_or_argument_changed": False,
            "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        }
    )
    atomic_json(GATE_JSON, gate)
    if not all_charts_accepted:
        raise RuntimeError("5127 outer-collinear pole-chart gate rejected")

    config = read_json(CONFIG)
    schedule_document = read_json(SCHEDULE)
    jobs = schedule_document["jobs"]
    job = next(row for row in jobs if row["job_key"] == JOB_KEY)
    module = problem["module"]
    manager = M5125.M5077.CentralTopologyManager(RUN, config)
    M5125.M5077.install_history_invariant_breakpoints(module)
    previous_catalog = M5125.M5077.certified_primary_catalog
    previous_global = module.global_chamber_value
    previous_breakpoints = module.collision_scaled_breakpoints
    extension = CertifiedOuterCollinearPoleChart(
        previous_global, problem["ownership"], charts
    )
    CATALOG_AUDIT.clear()
    M5126.REPAIR_AUDIT.clear()
    M5125.M5077.certified_primary_catalog = catalog_overlay(
        charts, problem["ownership"]
    )
    module.global_chamber_value = extension
    module.collision_scaled_breakpoints = chart_breakpoints(
        previous_breakpoints, charts
    )
    started = time.monotonic()
    try:
        row = M5125.execute_full_job(RUN, config, manager, job)
    finally:
        M5125.M5077.certified_primary_catalog = previous_catalog
        module.global_chamber_value = previous_global
        module.collision_scaled_breakpoints = previous_breakpoints
    replay_runtime = time.monotonic() - started

    if Path(row.get("kernel_file", WITNESS_KERNEL)).exists():
        kernel = read_json(Path(row.get("kernel_file", WITNESS_KERNEL)))
    else:
        kernel = {}
    profile_audit = dict(row.get("profile_audit", {}))
    profile_audit["same_sheet_outer_collinear_pole_chart"] = extension.summary()
    profile_audit["same_sheet_outer_collinear_catalog_rows"] = len(CATALOG_AUDIT)
    row.update(
        {
            "profile_audit": profile_audit,
            "repair_checkpoint_marker": MARKER,
            "repair_gate": relative(GATE_JSON),
            "repair_gate_sha256": digest(GATE_JSON),
        }
    )
    atomic_json(WITNESS_JOB, row)
    if kernel:
        kernel_profile = dict(kernel.get("profile_audit", {}))
        kernel_profile["same_sheet_outer_collinear_pole_chart"] = (
            extension.summary()
        )
        kernel_profile["same_sheet_outer_collinear_catalog_rows"] = len(
            CATALOG_AUDIT
        )
        kernel.update(
            {
                "profile_audit": kernel_profile,
                "repair_checkpoint_marker": MARKER,
                "repair_gate": relative(GATE_JSON),
                "repair_gate_sha256": digest(GATE_JSON),
            }
        )
        atomic_json(WITNESS_KERNEL, kernel)

    write_csv(CATALOG_CSV, CATALOG_AUDIT)
    fixed_gate = kernel.get("fixed_event_integral_gate", {})
    order_rows = fixed_gate.get("order_rows", [])
    highest = order_rows[-1] if order_rows else {}
    counts = M5125.run_counts(RUN, config["config_digest"], jobs)
    status = tagged(
        {
            "state": (
                "PAUSED_AFTER_5127_A00_REPLAY"
                if row.get("status") == "COMPLETED_CONVERGED"
                else "BLOCKED_5127_A00_REPLAY"
            ),
            "run_id": RUN.name,
            "job_key": JOB_KEY,
            "job_status": row.get("status"),
            "replay_runtime_seconds": replay_runtime,
            "expected_job_count": len(jobs),
            **counts,
            "chart_summary": extension.summary(),
            "catalog_row_count": len(CATALOG_AUDIT),
            "formalization_unchanged": tree_digest(FORMAL) == FORMAL_BASELINE,
        }
    )
    atomic_json(STATUS_JSON, status)
    atomic_json(RUN / "status.json", status)

    old_gate = problem["kernel"]["fixed_event_integral_gate"]
    old_order = old_gate["order_rows"][-1]
    result = tagged(
        {
            "job_key": JOB_KEY,
            "original_job": relative(ORIGINAL_JOB),
            "original_kernel": relative(ORIGINAL_KERNEL),
            "gate": relative(GATE_JSON),
            "catalog": relative(CATALOG_CSV),
            "old_status": problem["job"]["status"],
            "new_status": row.get("status"),
            "old_composite_interval_count": old_order[
                "composite_interval_count"
            ],
            "new_composite_interval_count": highest.get(
                "composite_interval_count"
            ),
            "old_maximum_adaptive_chamber_relative_error": old_order[
                "maximum_adaptive_chamber_relative_error"
            ],
            "new_maximum_adaptive_chamber_relative_error": highest.get(
                "maximum_adaptive_chamber_relative_error"
            ),
            "old_causally_corrected_value": old_order[
                "causally_corrected_value"
            ],
            "new_causally_corrected_value": highest.get(
                "causally_corrected_value"
            ),
            "normalized_direct_D_hhh_over_G3": row.get(
                "normalized_direct_D_hhh_over_G3"
            ),
            "chart_summary": extension.summary(),
            "catalog_rows": CATALOG_AUDIT,
            "run_counts": counts,
            "config_digest_preserved": row.get("config_digest")
            == problem["job"]["config_digest"],
            "profile_tolerance": config["tiers"]["primary24"]
            ["relative_adaptive_tolerance"],
            "profile_interval_cap": config["tiers"]["primary24"]
            ["relative_adaptive_maximum_intervals"],
            "formalization_workbench_tree_sha256": tree_digest(FORMAL),
            "interpretation": (
                "The A00 failure was a missing same-sheet outer-pole map, not "
                "an endpoint singularity. The replay is a numerical pipeline "
                "repair and is not a UV or MTS physics claim."
            ),
        }
    )
    atomic_json(RESULT_JSON, result)

    tolerance = float(
        config["tiers"]["primary24"]["relative_adaptive_tolerance"]
    )
    checks = [
        (
            "source_paths_exist",
            all(
                path.exists()
                for path in (
                    SCRIPT_5126,
                    ORIGINAL_JOB,
                    ORIGINAL_KERNEL,
                    GATE_JSON,
                    CATALOG_CSV,
                    WITNESS_JOB,
                    WITNESS_KERNEL,
                )
            ),
            "all 5127 source and witness paths exist",
        ),
        (
            "original_witness_preserved",
            problem["job"]["status"] == "COMPLETED_UNCONVERGED",
            problem["job"]["status"],
        ),
        (
            "four_derived_outer_poles",
            len(charts) == 4,
            str([(row["family"], row["member"]) for row in charts]),
        ),
        (
            "kinematic_root_conditions",
            all(
                chart["condition_residual"] < ROOT_RESIDUAL_TOLERANCE
                for chart in charts
            ),
            str(max(chart["condition_residual"] for chart in charts)),
        ),
        (
            "reciprocal_root_products",
            all(
                chart["reciprocal_root_residual"]
                < ROOT_RESIDUAL_TOLERANCE
                for chart in charts
            ),
            str(max(chart["reciprocal_root_residual"] for chart in charts)),
        ),
        (
            "simple_pole_laurent_order",
            all(
                chart["double_to_simple_ratio"]
                < MAXIMUM_DOUBLE_TO_SIMPLE_RATIO
                for chart in charts
            ),
            str(max(chart["double_to_simple_ratio"] for chart in charts)),
        ),
        (
            "boundary_residue_stability",
            all(
                chart["residue_disagreement"]
                < MAXIMUM_RESIDUE_DISAGREEMENT
                for chart in charts
            ),
            str(max(chart["residue_disagreement"] for chart in charts)),
        ),
        (
            "regular_part_uncertainty_bounded",
            all(
                chart["regular_integral_uncertainty"]
                < MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY
                for chart in charts
            ),
            str(
                max(chart["regular_integral_uncertainty"] for chart in charts)
            ),
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
            "A00_replay_converged",
            row.get("status") == "COMPLETED_CONVERGED"
            and bool(fixed_gate.get("fixed_event_crossed_integral_converged")),
            str(row.get("status")),
        ),
        (
            "adaptive_error_below_unchanged_tolerance",
            float(
                highest.get("maximum_adaptive_chamber_relative_error", math.inf)
            )
            <= tolerance,
            str(highest.get("maximum_adaptive_chamber_relative_error")),
        ),
        (
            "interval_count_reduced",
            int(highest.get("composite_interval_count", 10**9))
            < int(old_order["composite_interval_count"]),
            f"old={old_order['composite_interval_count']};new={highest.get('composite_interval_count')}",
        ),
        (
            "locked_profile_preserved",
            result["config_digest_preserved"]
            and result["profile_tolerance"] == 5.0e-5
            and result["profile_interval_cap"] == 4096,
            f"digest={result['config_digest_preserved']};tol={result['profile_tolerance']};cap={result['profile_interval_cap']}",
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
            "pipeline repair only",
        ),
    ]
    write_csv(VALIDATION_CSV, validation_rows(checks))
    failures = [name for name, passed, _ in checks if not passed]
    if failures:
        raise RuntimeError(f"5127 validation failed: {failures}")
    write_document(result)
    return result


def write_document(result: dict[str, Any]) -> None:
    rows = result["catalog_rows"]
    pole_lines = "\n".join(
        f"- `{row['family']}:{row['member']}`: `q={row['root']}`, "
        f"`Res={row['residue']}`, path distance `{row['log_distance']:.6g}`."
        for row in rows
    )
    text = f"""# 5127 - same-sheet outer-collinear pole chart and A00 replay

## What the failed integration was actually seeing

The endpoint-adjacent direct-`g1` collisions are removable double-zero
collisions, but they were not the dominant A00 error. Two symmetric interior
intervals contain four genuine outer simple poles that checkpoint 5030 could
not catalogue because it searched only opposite-ownership global-root
collisions.

The missing roots are derived before replay from

```text
C(q)=c_s c_d+s_s s_d(q+q^-1)/2.
```

The beam-spinor family satisfies `p_1^-=E_1-p_1z=0`. The hard-soft family
satisfies

```text
s_13 = 2 e A (1+beta) (1-C) = 0.
```

Each condition is a quadratic in `q` with reciprocal roots. No root, event,
seed or fit parameter was inferred from the desired integral value.

## Guarded numerical continuation

For each isolated root `z0=log(q0)`, the integrated global cycle is written

```text
F(z) = R/(z-z0) + H(z).
```

`R` is measured on an isolated high-precision Cauchy boundary. The absence of
a material second principal coefficient checks the simple-pole order. The
regular part `H` is reconstructed by Cauchy's formula only inside 65% of that
boundary radius; outside it the original evaluator is used. The pole is
subtracted in the adaptive integrand and integrated analytically. No principal
value or half residue is inserted.

{pole_lines}

## Exact replay

The locked A00 row changes from `{result['old_status']}` to
`{result['new_status']}`. Its interval count changes from
`{result['old_composite_interval_count']}` to
`{result['new_composite_interval_count']}`, and the maximum chamber error
changes from `{result['old_maximum_adaptive_chamber_relative_error']}` to
`{result['new_maximum_adaptive_chamber_relative_error']}` under the unchanged
`5e-5` tolerance and 4096-interval cap.

The new causally corrected value is
`{result['new_causally_corrected_value']}`. It remains private nonclaim pilot
data. Checkpoint 5127 repairs a missing analytic stratum in the numerical
contour map; it does not establish the UV coefficient, source coupling,
local GR/Newton, Maxwell, galactic dynamics or full MTS.

The machine/cog condition is unchanged: one parent theory must preserve the
tested local GR/Newton cogs while deriving galactic activation without a
manual regime switch.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    arguments = parser.parse_args()
    if arguments.execute:
        result = execute()
    else:
        result = structural_dry_run()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
