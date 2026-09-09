from __future__ import annotations

import csv
import ctypes
from datetime import datetime, timezone
import importlib.util
import json
import math
import os
from pathlib import Path
import time
from typing import Any


for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ[variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5449"
FORMALIZATION = POST.parent / "formalization-workbench"

PARENT_SCRIPT = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
EVENTS = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
MAPPED_CELLS = FUNCTIONAL_RG / "5393" / "D4_parent_frozen_mapped_cells.csv"
ANALYTICITY_RESULT = FUNCTIONAL_RG / "5448" / "D4_event_local_analyticity_result.json"

DOCUMENT = POST / "5449-Y5-R2FR-D4-event-local-finite-enclosure-smoke.md"
PROBES = OUTPUT / "D4_event_local_interior_enclosure_probes.csv"
OWNERS = OUTPUT / "D4_event_local_cell_term_owner_manifest.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5449_VALIDATION.csv"
RESULT = OUTPUT / "D4_event_local_finite_enclosure_smoke_result.json"

CHECKPOINT = 5449
REVISION = "D4-event-local-finite-enclosure-smoke-v1"
EPSILON_CENTERS = (0.005, 0.015)
PATH_SEGMENTS = ("LEFT_CONNECTOR", "TOP", "RIGHT_CONNECTOR")
EPSILON_HALF_WIDTH = 1.0e-8
X_HALF_WIDTH_MAX = 1.0e-8
PATH_HALF_WIDTH = 0.01


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
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    fields = list(rows[0])
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def owner_manifest() -> list[dict[str, Any]]:
    events = read_csv(EVENTS)
    cells = [
        row for row in read_csv(MAPPED_CELLS) if row["region_class"] == "EVENT_TUBE"
    ]
    rows: list[dict[str, Any]] = []
    for event in events:
        matches = [
            cell
            for cell in cells
            if cell["event_id"] == event["event_id"]
            and event["term_id"] in cell["reduced_MC04_term_ids"].split("|")
        ]
        for cell in matches:
            lower = float(cell["lower_absolute_soft_cosine"])
            upper = float(cell["upper_absolute_soft_cosine"])
            coordinate = float(event["zero_regulator_absolute_soft_cosine"])
            rows.append(
                {
                    "event_id": event["event_id"],
                    "event_type": event["event_type"],
                    "term_id": event["term_id"],
                    "primary_surface_id": event["primary_surface_id"],
                    "mapped_cell_id": cell["mapped_cell_id"],
                    "cell_lower_absolute_soft_cosine": lower,
                    "cell_upper_absolute_soft_cosine": upper,
                    "zero_regulator_event_coordinate": coordinate,
                    "event_coordinate_inside_cell": lower <= coordinate <= upper,
                    "lower_energy_boundary": cell["lower_energy_boundary"],
                    "upper_energy_boundary": cell["upper_energy_boundary"],
                    "owner_status": "EVENT_TERM_CELL_INTERIOR_SMOKE_OWNER",
                    "valid_for_D4_event_local_interior_smoke": False,
                    "valid_for_D4_event_local_W3_bound": False,
                    "valid_for_D4_numeric_W3_bound": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def probe_rows(parent: Any, owners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cells = {row["mapped_cell_id"]: row for row in parent.read_csv(parent.MAPPED_5393)}
    support_segments = parent.material_support_segments()
    branches = parent.material_branch_data()
    rows: list[dict[str, Any]] = []
    for owner in owners:
        cell = cells[owner["mapped_cell_id"]]
        term_id = owner["term_id"]
        configurations = parent.configuration_variants(term_id)
        coordinate = float(owner["zero_regulator_event_coordinate"])
        cell_width = float(owner["cell_upper_absolute_soft_cosine"]) - float(
            owner["cell_lower_absolute_soft_cosine"]
        )
        x_half_width = min(X_HALF_WIDTH_MAX, 1.0e-4 * cell_width)
        x_lower = max(
            float(owner["cell_lower_absolute_soft_cosine"]),
            coordinate - x_half_width,
        )
        x_upper = min(
            float(owner["cell_upper_absolute_soft_cosine"]),
            coordinate + x_half_width,
        )
        for epsilon_index, epsilon_center in enumerate(EPSILON_CENTERS):
            epsilon_row = {
                "regulator_bin_index": epsilon_index,
                "epsilon_subdivision_index": 0,
                "epsilon_subdivision_count": 1,
                "epsilon_real_lower": epsilon_center - EPSILON_HALF_WIDTH,
                "epsilon_real_upper": epsilon_center + EPSILON_HALF_WIDTH,
                "epsilon_imaginary_lower": -EPSILON_HALF_WIDTH,
                "epsilon_imaginary_upper": EPSILON_HALF_WIDTH,
            }
            for path_segment in PATH_SEGMENTS:
                started = time.time()
                base = {
                    "event_id": owner["event_id"],
                    "event_type": owner["event_type"],
                    "mapped_cell_id": owner["mapped_cell_id"],
                    "term_id": term_id,
                    "epsilon_center": epsilon_center,
                    "epsilon_half_width": EPSILON_HALF_WIDTH,
                    "path_segment": path_segment,
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "path_parameter_lower": 0.5 - PATH_HALF_WIDTH,
                    "path_parameter_upper": 0.5 + PATH_HALF_WIDTH,
                }
                try:
                    result = parent.evaluate_path_box(
                        cell,
                        term_id,
                        configurations,
                        epsilon_row,
                        path_segment,
                        x_lower,
                        x_upper,
                        0.5 - PATH_HALF_WIDTH,
                        0.5 + PATH_HALF_WIDTH,
                        0,
                        "EVENT_LOCAL_INTERIOR_SMOKE",
                        support_segments,
                        branches,
                        4,
                    )
                    finite_values = (
                        float(result["integrated_regular_path_abs_upper"]),
                        float(result["minimum_amplitude_denominator_abs_lower"]),
                        float(result["collision_jacobian_abs_lower"]),
                    )
                    passed = (
                        all(math.isfinite(value) for value in finite_values)
                        and finite_values[0] > 0.0
                        and finite_values[1] > 0.0
                        and finite_values[2] > 0.0
                    )
                    rows.append(
                        {
                            **base,
                            "probe_passed": passed,
                            "failure_type": "",
                            "failure_message": "",
                            "integrated_regular_path_abs_upper": finite_values[0],
                            "minimum_amplitude_denominator_abs_lower": finite_values[1],
                            "collision_jacobian_abs_lower": finite_values[2],
                            "path_integral_enclosure_method": result.get(
                                "path_integral_enclosure_method", ""
                            ),
                            "runtime_seconds": time.time() - started,
                            "valid_for_D4_event_local_interior_smoke": passed,
                            "valid_for_D4_event_local_W3_bound": False,
                            "valid_for_D4_numeric_W3_bound": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
                except Exception as error:
                    rows.append(
                        {
                            **base,
                            "probe_passed": False,
                            "failure_type": type(error).__name__,
                            "failure_message": str(error).splitlines()[0][:300],
                            "integrated_regular_path_abs_upper": math.nan,
                            "minimum_amplitude_denominator_abs_lower": math.nan,
                            "collision_jacobian_abs_lower": math.nan,
                            "path_integral_enclosure_method": "",
                            "runtime_seconds": time.time() - started,
                            "valid_for_D4_event_local_interior_smoke": False,
                            "valid_for_D4_event_local_W3_bound": False,
                            "valid_for_D4_numeric_W3_bound": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
    return rows


def render_document(payload: dict[str, Any], probes: list[dict[str, Any]]) -> None:
    failures: dict[str, int] = {}
    for row in probes:
        if not row["probe_passed"]:
            label = f"{row['failure_type']}:{row['failure_message']}"
            failures[label] = failures.get(label, 0) + 1
    lines = [
        "# 5449: D4 event-local finite-enclosure smoke",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "Checkpoint 5448 proves that the singular `H log + G` primitive can be removed without leaving a hidden nonanalytic term. This checkpoint asks a narrower executable question: can the unchanged parent interval evaluator produce finite positive enclosures in small closed interior boxes around every event owner, on both regulator halves and all three deformed contour segments?",
        "",
        "## Smoke matrix",
        "",
        f"- event-cell/term owners: `{payload['event_cell_term_owner_count']}`;",
        f"- closed interval probes: `{payload['probe_count']}`;",
        f"- passed probes: `{payload['passed_probe_count']}`;",
        f"- failed probes: `{payload['failed_probe_count']}`;",
        f"- minimum positive amplitude denominator: `{payload['minimum_amplitude_denominator_abs_lower']}`;",
        f"- minimum positive collision Jacobian: `{payload['minimum_collision_jacobian_abs_lower']}`.",
        "",
        "## Failure classes",
        "",
    ]
    if failures:
        for label, count in sorted(failures.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"- `{label}`: `{count}`;")
    else:
        lines.append("- none on the declared interior smoke boxes;")
    lines.extend(
        [
            "",
            "## Consequence",
            "",
            "A pass proves neither endpoint coverage nor the event-local `W3` bound. It does show that no new interior singular class appears when the existing parent evaluator is moved from away cells onto all event owners. The next proof can therefore focus on the endpoint neighborhoods and the explicit nonsingular upper primitive instead of replacing the parent amplitude machinery.",
            "",
            "The production construction must expand these seed boxes into a finite closed cover, add the exact event principal-part subtraction on connector endpoints, and aggregate the resulting complex-strip suprema with the checkpoint-5448 Cauchy formula.",
            "",
            "## Claim boundary",
            "",
            "All event-local `W3`, combined `W3`, regulator-limit, all-operator local-GR and full-MTS flags remain false.",
            "",
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines))


def run() -> dict[str, Any]:
    set_below_normal_priority()
    started_utc = datetime.now(timezone.utc)
    started = time.time()
    analytic = read_json(ANALYTICITY_RESULT)
    owners = owner_manifest()
    parent = load_module("mts_5396_for_5449", PARENT_SCRIPT)
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    probes = probe_rows(parent, owners)
    passed = [row for row in probes if row["probe_passed"]]
    failed = [row for row in probes if not row["probe_passed"]]
    expected_probe_count = len(owners) * len(EPSILON_CENTERS) * len(PATH_SEGMENTS)
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "ALL_EVENT_OWNER_INTERIOR_ENCLOSURES_FINITE__PROCEED_TO_ENDPOINT_COVER"
            if not failed
            else "EVENT_OWNER_INTERIOR_SMOKE_EXPOSES_CLASSES__CLASSIFY_BEFORE_ENDPOINT_COVER"
        ),
        "parent_revision": parent.REVISION,
        "event_cell_term_owner_count": len(owners),
        "probe_count": len(probes),
        "expected_probe_count": expected_probe_count,
        "passed_probe_count": len(passed),
        "failed_probe_count": len(failed),
        "failure_classes": sorted(
            {
                f"{row['failure_type']}:{row['failure_message']}" for row in failed
            }
        ),
        "minimum_amplitude_denominator_abs_lower": min(
            (float(row["minimum_amplitude_denominator_abs_lower"]) for row in passed),
            default=math.nan,
        ),
        "minimum_collision_jacobian_abs_lower": min(
            (float(row["collision_jacobian_abs_lower"]) for row in passed),
            default=math.nan,
        ),
        "runtime_seconds": time.time() - started,
        "next_target": (
            "EVENT_ENDPOINT_PRINCIPAL_PART_SUBTRACTION_AND_FINITE_COVER"
            if not failed
            else "CLASSIFY_EVENT_INTERIOR_FAILURES"
        ),
        "valid_for_D4_event_local_interior_smoke": not failed,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_D4_numeric_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }

    validations = [
        check("all_sources_exist", all(path.is_file() for path in (PARENT_SCRIPT, EVENTS, MAPPED_CELLS, ANALYTICITY_RESULT)), "parent+events+mapped cells+5448"),
        check("event_local_analyticity_is_certified", analytic.get("all_event_remainders_holomorphic") is True and analytic.get("failed_validation_count") == 0, analytic.get("decision")),
        check("all_event_coordinates_lie_in_owned_cells", owners and all(row["event_coordinate_inside_cell"] for row in owners), len(owners)),
        check("probe_matrix_is_complete", len(probes) == expected_probe_count, f"{len(probes)}/{expected_probe_count}"),
        check("every_event_has_an_owner_probe", {row["event_id"] for row in probes} == {f"E{index:02d}" for index in range(1, 9)}, sorted({row["event_id"] for row in probes})),
        check("all_interior_enclosures_are_finite", not failed, payload["failure_classes"]),
        check("all_positive_margins_remain_positive", passed and all(float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0 and float(row["collision_jacobian_abs_lower"]) > 0.0 for row in passed), f"passed={len(passed)}"),
        check("broad_claims_remain_false", not payload["valid_for_D4_event_local_W3_bound"] and not payload["valid_for_D4_numeric_W3_bound"] and not payload["valid_for_all_operator_local_GR_claim"] and not payload["valid_for_full_MTS_claim"], "interior smoke only"),
    ]
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started_utc
    ]
    validations.append(check("formalization_workbench_untouched", not formalization_touches, f"modified_file_count={len(formalization_touches)}"))
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    for owner in owners:
        owner["valid_for_D4_event_local_interior_smoke"] = not failed
    atomic_csv(OWNERS, owners)
    atomic_csv(PROBES, probes)
    atomic_csv(VALIDATION, validations)
    render_document(payload, probes)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
