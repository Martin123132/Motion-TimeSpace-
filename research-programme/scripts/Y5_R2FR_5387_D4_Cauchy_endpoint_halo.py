from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
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
SCRIPT_5380 = SCRIPTS / "Y5_R2FR_5380_D4_complexified_event_neighborhood_certificate.py"
BASE_BOXES = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
EVENTS = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
OUTPUT = FUNCTIONAL_RG / "5387"
DOCUMENT = POST / "5387-Y5-R2FR-D4-Cauchy-endpoint-halo.md"
LOWER_HALO = (-1.0e-6, 1.0e-6)
UPPER_HALO = (0.019999, 0.020001)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5380 = load_module("mts_5380_for_5387", SCRIPT_5380)


def parse_real_bounds(text: str) -> tuple[float, float]:
    lower, upper = text.strip()[1:-1].split(",")
    return float(lower), float(upper)


def parse_complex_box(text: str) -> Any:
    real_text, imaginary_text = text.split("+i")
    real_lower, real_upper = parse_real_bounds(real_text)
    imaginary_lower, imaginary_upper = parse_real_bounds(imaginary_text)
    return M5380.complex_box(
        real_lower,
        real_upper,
        imaginary_lower,
        imaginary_upper,
    )


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5387 — Y5/R2FR D4 Cauchy endpoint halo",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Certificate",
        "",
        f"- certified halo boxes: `{result['certified_box_count']}/{result['required_box_count']}`;",
        f"- lower real halo: `{LOWER_HALO}`;",
        f"- upper real halo: `{UPPER_HALO}`;",
        f"- imaginary half-width: `{M5380.EPSILON_IMAGINARY_HALF_WIDTH}`;",
        f"- minimum strict Krawczyk inclusion margin: `{result['minimum_inclusion_margin']}`;",
        f"- maximum contraction bound: `{result['maximum_contraction_bound']}`.",
        "",
        "## Scope",
        "",
        "These boxes extend the certified event branches far enough to place radius-5e-7 Cauchy circles around both real endpoints of [0,0.02]. They do not by themselves bound the finite-plus contour integrand or establish H3; those gates remain false until the contour sweep covers the halo rows.",
        "",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    M5380.set_below_normal_priority()
    M5380.mp.mp.dps = M5380.MP_DIGITS
    iv.dps = M5380.INTERVAL_DIGITS
    references, _ = M5380.M5379.M5378.M5359.reference_rows()
    events = {row["event_id"]: row for row in M5380.read_csv(EVENTS)}
    base_rows = M5380.read_csv(BASE_BOXES)
    base_lookup = {
        (row["event_id"], int(row["epsilon_bin_index"])): row
        for row in base_rows
    }
    rows: list[dict[str, Any]] = []
    for event_id in M5380.EVENT_IDS:
        configuration = M5380.M5379.M5378.M5359.event_configuration(
            events[event_id], references
        )
        zero_coordinate = M5380.mp.mpf(
            events[event_id]["zero_regulator_absolute_soft_cosine"]
        )
        for halo_id, epsilon_bounds, source_bin in (
            (-1, LOWER_HALO, 0),
            (8, UPPER_HALO, 7),
        ):
            source = base_lookup[(event_id, source_bin)]
            initial_state_boxes = [
                parse_complex_box(text)
                for text in source["complex_state_boxes"].split("|")
            ]
            midpoint = 0.5 * sum(epsilon_bounds)
            center = M5380.point_solution(
                configuration, midpoint, zero_coordinate
            )
            state_boxes, certificate, inflation_steps = (
                M5380.construct_certified_state_box(
                    configuration,
                    epsilon_bounds,
                    initial_state_boxes,
                    center,
                )
            )
            rows.append(
                {
                    "event_id": event_id,
                    "event_type": configuration["event_type"],
                    "epsilon_bin_index": halo_id,
                    "epsilon_real_lower": epsilon_bounds[0],
                    "epsilon_real_upper": epsilon_bounds[1],
                    "epsilon_imaginary_lower": -M5380.EPSILON_IMAGINARY_HALF_WIDTH,
                    "epsilon_imaginary_upper": M5380.EPSILON_IMAGINARY_HALF_WIDTH,
                    "complex_system_dimension": len(state_boxes),
                    "state_box_inflation_iterations": inflation_steps,
                    "complex_state_boxes": "|".join(
                        M5380.complex_interval_text(value)
                        for value in state_boxes
                    ),
                    "complex_Krawczyk_images": "|".join(
                        M5380.complex_interval_text(value)
                        for value in certificate["operator"]
                    ),
                    "minimum_strict_inclusion_margin": certificate[
                        "minimum_inclusion_margin"
                    ],
                    "maximum_contraction_bound": certificate[
                        "contraction_bound"
                    ],
                    "point_jacobian_condition_number": certificate[
                        "point_jacobian_condition_number"
                    ],
                    "complex_neighborhood_box_passes": certificate["passes"],
                    "valid_for_D4_Cauchy_endpoint_halo": certificate["passes"],
                    "valid_for_D4_numeric_H3_bound": False,
                    "valid_for_D4_numeric_uniform_remainder_bound": False,
                    "valid_for_D4_outer_regulator_zero_limit": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    required = 2 * len(M5380.EVENT_IDS)
    certified = sum(
        row["complex_neighborhood_box_passes"] is True for row in rows
    )
    result = {
        "checkpoint": 5387,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "runtime_seconds": time.perf_counter() - started,
        "required_box_count": required,
        "certified_box_count": certified,
        "minimum_inclusion_margin": min(
            float(row["minimum_strict_inclusion_margin"]) for row in rows
        ),
        "maximum_contraction_bound": max(
            float(row["maximum_contraction_bound"]) for row in rows
        ),
        "validation_passed": certified == required,
        "decision": (
            "CAUCHY_ENDPOINT_HALO_CERTIFIED__RUN_NESTED_CONTOUR_ENCLOSURE"
            if certified == required
            else "CAUCHY_ENDPOINT_HALO_BLOCKED"
        ),
        "claim_boundary": {
            "valid_for_D4_Cauchy_endpoint_halo": certified == required,
            "valid_for_D4_numeric_H3_bound": False,
            "valid_for_D4_numeric_uniform_remainder_bound": False,
            "valid_for_D4_outer_regulator_zero_limit": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    }
    output.mkdir(parents=True, exist_ok=True)
    M5380.atomic_csv(output / "D4_Cauchy_endpoint_halo_boxes.csv", rows)
    M5380.atomic_json(output / "D4_Cauchy_endpoint_halo_result.json", result)
    (output / "status.json").write_text(
        json.dumps(
            {
                "state": "complete" if certified == required else "blocked",
                "updated_utc": result["updated_utc"],
                "certified_box_count": certified,
                "required_box_count": required,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
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
