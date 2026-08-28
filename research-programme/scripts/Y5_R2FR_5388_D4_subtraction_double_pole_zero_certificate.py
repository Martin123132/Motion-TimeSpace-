from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any

from mpmath import iv


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


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5388"
DOCUMENT = POST / "5388-Y5-R2FR-D4-subtraction-double-pole-zero.md"
SCRIPT_5385 = (
    SCRIPTS
    / "Y5_R2FR_5385_D4_expanded_energy_contour_full_pole_catalog_clearance.py"
)
HALO_BOXES = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_boxes.csv"
BASE_ROOTS = (
    FUNCTIONAL_RG
    / "5385"
    / "D4_expanded_energy_full_catalog_clearance_roots.csv"
)
RESULT_5385 = (
    FUNCTIONAL_RG
    / "5385"
    / "D4_expanded_energy_full_catalog_clearance_result.json"
)
RESULT_5019 = (
    FUNCTIONAL_RG
    / "5019"
    / "hhh_exact_soft_endpoint_and_crossed_pole_results.json"
)
ENERGY_ARC_COUNT = 32
EXPECTED_HALO_BOXES = 16
NONACTIVE_SUBTRACTION_ROOTS_PER_ARC = 7


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5385 = load_module("mts_5385_for_subtraction_zero", SCRIPT_5385)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5388 — Y5/R2FR D4 subtraction double-pole zero",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Derivation",
        "",
        "The finite-plus endpoint subtraction is not silently discarded. Checkpoint 5019 proves that its crossed azimuth singularities are simple poles. Checkpoint 5385 identifies exactly one subtraction root at the selected global center and excludes the other seven subtraction roots throughout the base complex strip.",
        "",
        "This checkpoint repeats the seven-root exclusion on both complex endpoint halos for every one of the 32 expanded energy-contour arcs. A meromorphic term with at most a simple pole at z=z_star has Laurent form a_-1/(z-z_star)+sum_(n>=0) a_n(z-z_star)^n. Its (z-z_star)^-2 coefficient is therefore exactly zero, so the endpoint subtraction contributes zero to H_k.",
        "",
        f"- halo boxes: `{result['halo_box_count']}`;",
        f"- halo energy arcs: `{result['halo_arc_count']}`;",
        f"- checked nonactive subtraction-root rows: `{result['halo_root_summary_count']}`;",
        f"- minimum halo subtraction-root clearance: `{result['minimum_halo_clearance_margin_lower']}`.",
        "",
        "## Scope",
        "",
        "The result removes only the subtraction term from the global double-pole coefficient. It does not remove the subtraction from other finite coefficients, G3, W3, or the full integral. H3 remains false until the direct nested-contour matrix and Cauchy aggregation pass.",
        "",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    iv.dps = M5385.INTERVAL_DIGITS
    halo_rows = read_csv(HALO_BOXES)
    base_rows = read_csv(BASE_ROOTS)
    result_5385 = json.loads(RESULT_5385.read_text(encoding="utf-8"))
    result_5019 = json.loads(RESULT_5019.read_text(encoding="utf-8"))
    references, _ = M5385.M5380.M5379.M5378.M5359.reference_rows()
    events = {
        row["event_id"]: row for row in read_csv(M5385.EVENTS_5358)
    }
    configurations = {
        event_id: M5385.M5380.M5379.M5378.M5359.event_configuration(
            event, references
        )
        for event_id, event in events.items()
    }
    arc_rows: list[dict[str, Any]] = []
    root_aggregate: dict[tuple[str, int, str], dict[str, Any]] = {}
    for source in halo_rows:
        configuration = configurations[source["event_id"]]
        epsilon = iv.mpc(
            iv.mpf(
                [source["epsilon_real_lower"], source["epsilon_real_upper"]]
            ),
            iv.mpf(
                [
                    source["epsilon_imaginary_lower"],
                    source["epsilon_imaginary_upper"],
                ]
            ),
        )
        state_boxes = [
            M5385.M5381.parse_complex_box(text)
            for text in source["complex_state_boxes"].split("|")
        ]
        inputs = M5385.event_inputs(configuration, epsilon, state_boxes)
        active_root_id = (
            "subtraction:soft:" + configuration["root_labels"][1]
        )
        for arc_index in range(ENERGY_ARC_COUNT):
            phase = (
                2
                * iv.pi
                * iv.mpf([arc_index, arc_index + 1])
                / ENERGY_ARC_COUNT
            )
            energy_displacement = iv.mpf(
                M5385.ENERGY_CONTOUR_RELATIVE_RADIUS
            ) * (iv.cos(phase) + 1j * iv.sin(phase))
            geometry = M5385.expanded_geometry(
                configuration, inputs, energy_displacement
            )
            selected_root = geometry["selected_root"]
            global_radius_upper = float(
                M5385.GLOBAL_CONTOUR_RELATIVE_RADIUS
            ) * max(1.0, M5385.M5381.modulus_upper(selected_root))
            records: list[dict[str, Any]] = []
            active_count = 0
            for source_name, factors in (
                ("subtraction:soft", geometry["soft_factors"]),
                ("subtraction:decay", geometry["decay_factors"]),
            ):
                for label in M5385.M5384.GLOBAL_ROOT_LABELS:
                    root_id = f"{source_name}:{label}"
                    if root_id == active_root_id:
                        active_count += 1
                        continue
                    bound = M5385.M5384.projective_separation_bound(
                        factors,
                        label,
                        inputs["external_root"],
                        selected_root,
                    )
                    margin = (
                        float(bound["separation_modulus_lower"])
                        - global_radius_upper
                    )
                    record = {
                        "root_id": root_id,
                        "method": bound["method"],
                        "chart": bound["chart"],
                        "separation_modulus_lower": float(
                            bound["separation_modulus_lower"]
                        ),
                        "clearance_margin_lower": margin,
                        "root_clears_global_contour": margin > 0,
                    }
                    records.append(record)
                    aggregate_key = (
                        configuration["event_id"],
                        int(source["epsilon_bin_index"]),
                        root_id,
                    )
                    aggregate = root_aggregate.get(aggregate_key)
                    if aggregate is None:
                        root_aggregate[aggregate_key] = {
                            "event_id": configuration["event_id"],
                            "event_type": configuration["event_type"],
                            "epsilon_bin_index": int(
                                source["epsilon_bin_index"]
                            ),
                            "root_id": root_id,
                            "minimum_separation_modulus_lower": float(
                                bound["separation_modulus_lower"]
                            ),
                            "minimum_clearance_margin_lower": margin,
                            "worst_energy_phase_arc_index": arc_index,
                            "all_energy_arcs_clear": margin > 0,
                        }
                    else:
                        aggregate["all_energy_arcs_clear"] = (
                            aggregate["all_energy_arcs_clear"] and margin > 0
                        )
                        if margin < aggregate["minimum_clearance_margin_lower"]:
                            aggregate["minimum_separation_modulus_lower"] = float(
                                bound["separation_modulus_lower"]
                            )
                            aggregate["minimum_clearance_margin_lower"] = margin
                            aggregate["worst_energy_phase_arc_index"] = arc_index
            arc_rows.append(
                {
                    "event_id": configuration["event_id"],
                    "event_type": configuration["event_type"],
                    "epsilon_bin_index": int(source["epsilon_bin_index"]),
                    "energy_phase_arc_index": arc_index,
                    "active_subtraction_root_id": active_root_id,
                    "active_subtraction_root_count": active_count,
                    "nonactive_subtraction_root_count": len(records),
                    "minimum_clearance_margin_lower": min(
                        row["clearance_margin_lower"] for row in records
                    ),
                    "all_nonactive_subtraction_roots_clear": all(
                        row["root_clears_global_contour"] for row in records
                    ),
                }
            )
    root_rows = sorted(
        root_aggregate.values(),
        key=lambda row: (
            row["event_id"],
            row["epsilon_bin_index"],
            row["root_id"],
        ),
    )
    base_subtraction_rows = [
        row for row in base_rows if row["root_id"].startswith("subtraction:")
    ]
    base_groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in base_subtraction_rows:
        base_groups.setdefault(
            (row["event_id"], row["epsilon_bin_index"]), []
        ).append(row)
    crossed_poles = result_5019.get("crossed_poles", {})
    validations = {
        "checkpoint_5019_proves_simple_endpoint_poles": result_5019.get(
            "validation_all_passed"
        )
        is True
        and result_5019.get("exact_hhh_soft_endpoint_complete") is True
        and crossed_poles.get("all_exact_and_root_tracking_passed") is True
        and "simple" in str(crossed_poles.get("reason", "")).lower(),
        "checkpoint_5385_full_catalog_passes": result_5385.get(
            "validation_passed"
        )
        is True,
        "base_strip_has_seven_clear_nonactive_subtraction_roots_per_box": bool(
            base_groups
        )
        and all(
            len(group) == NONACTIVE_SUBTRACTION_ROOTS_PER_ARC
            and all(
                str(row["all_energy_arcs_clear"]).lower() == "true"
                and float(row["minimum_clearance_margin_lower"]) > 0
                for row in group
            )
            for group in base_groups.values()
        ),
        "all_sixteen_endpoint_halo_boxes_are_checked": len(halo_rows)
        == EXPECTED_HALO_BOXES,
        "every_halo_arc_has_exactly_one_active_subtraction_root": all(
            row["active_subtraction_root_count"] == 1 for row in arc_rows
        ),
        "every_halo_arc_has_seven_nonactive_subtraction_roots": all(
            row["nonactive_subtraction_root_count"]
            == NONACTIVE_SUBTRACTION_ROOTS_PER_ARC
            for row in arc_rows
        ),
        "all_halo_nonactive_subtraction_roots_clear": all(
            row["all_nonactive_subtraction_roots_clear"] for row in arc_rows
        ),
        "halo_root_summary_matrix_is_complete": len(root_rows)
        == EXPECTED_HALO_BOXES * NONACTIVE_SUBTRACTION_ROOTS_PER_ARC,
    }
    validation_passed = all(validations.values())
    validation_rows = [
        {"gate": gate, "passed": passed, "detail": str(passed)}
        for gate, passed in validations.items()
    ]
    minimum_halo_margin = min(
        row["minimum_clearance_margin_lower"] for row in root_rows
    )
    result = {
        "checkpoint": 5388,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "runtime_seconds": time.perf_counter() - started,
        "halo_box_count": len(halo_rows),
        "halo_arc_count": len(arc_rows),
        "halo_root_summary_count": len(root_rows),
        "minimum_halo_clearance_margin_lower": minimum_halo_margin,
        "subtraction_selected_global_pole_order_upper": (
            1 if validation_passed else None
        ),
        "subtraction_double_pole_coefficient": (
            0 if validation_passed else None
        ),
        "validation_passed": validation_passed,
        "validation": validations,
        "decision": (
            "SUBTRACTION_DOUBLE_POLE_COEFFICIENT_IDENTICALLY_ZERO__DIRECT_TERM_OWNS_H"
            if validation_passed
            else "SUBTRACTION_DOUBLE_POLE_ZERO_BLOCKED"
        ),
        "claim_boundary": {
            "valid_for_D4_subtraction_double_pole_zero": validation_passed,
            "valid_for_D4_numeric_H3_bound": False,
            "valid_for_D4_numeric_uniform_remainder_bound": False,
            "valid_for_D4_outer_regulator_zero_limit": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    }
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_subtraction_halo_clearance_arcs.csv", arc_rows)
    atomic_csv(output / "D4_subtraction_halo_clearance_roots.csv", root_rows)
    atomic_csv(output / "D4_subtraction_double_pole_zero_validation.csv", validation_rows)
    atomic_json(output / "D4_subtraction_double_pole_zero_result.json", result)
    render_document(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    result = run(arguments.output.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
