from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
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


POST = Path(__file__).resolve().parents[1]
SCRIPT_5386 = POST / "scripts" / "Y5_R2FR_5386_D4_nested_contour_integrand_enclosure.py"
DEFAULT_ENERGY_ARCS = 32
DEFAULT_GLOBAL_ARCS = 1


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5386 = load_module("mts_5386_for_H3_augmentation", SCRIPT_5386)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def upward(value: float) -> float:
    return math.nextafter(float(value), math.inf)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def read_rows(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def row_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row["event_id"],
        int(row["epsilon_bin_index"]),
        int(row["epsilon_subdivision_index"]),
        int(row["energy_phase_arc_index"]),
        int(row["global_phase_arc_index"]),
    )


def compact_full(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": result["event_id"],
        "epsilon_bin_index": result["epsilon_bin_index"],
        "epsilon_subdivision_index": result["epsilon_subdivision_index"],
        "epsilon_subdivision_count": result["epsilon_subdivision_count"],
        "energy_phase_arc_index": result["energy_phase_arc_index"],
        "energy_phase_arc_count": result["energy_phase_arc_count"],
        "global_phase_arc_index": result["global_phase_arc_index"],
        "global_phase_arc_count": result["global_phase_arc_count"],
        "value_abs_upper": result["value_abs_upper"],
        "event_integrand_abs_upper_without_physical_multiplier": result[
            "event_integrand_abs_upper_without_physical_multiplier"
        ],
        "relative_root_modulus_lower": result[
            "geometric_factor_modulus_lowers"
        ]["relative_root"],
        "selected_global_root_modulus_lower": result[
            "geometric_factor_modulus_lowers"
        ]["selected_global_root"],
        "collision_jacobian_modulus_lower": result[
            "geometric_factor_modulus_lowers"
        ]["collision_jacobian"],
        "collision_jacobian_chart": result["geometric_path_diagnostics"][
            "collision_jacobian_chart"
        ],
        "collision_jacobian_chart_denominator_lower": result[
            "geometric_path_diagnostics"
        ]["collision_jacobian_chart_denominator_lower"],
        "collision_jacobian_recoil_derivative_upper": result[
            "geometric_path_diagnostics"
        ]["collision_jacobian_recoil_derivative_upper"],
        "minimum_denominator_lower": result["minimum_denominator_lower"],
        "energy_channel_quotient_abs_lower": result[
            "energy_channel_quotient_abs_lower"
        ],
        "left_active_invariant_abs_lower": result[
            "left_active_invariant_abs_lower"
        ],
        "parent_value_is_in_nested_interval": result[
            "parent_value_is_in_nested_interval"
        ],
        "nested_interval_relative_width": result[
            "nested_interval_relative_width"
        ],
        "nested_real_lower": result["nested_real_lower"],
        "nested_real_upper": result["nested_real_upper"],
        "nested_imaginary_lower": result["nested_imaginary_lower"],
        "nested_imaginary_upper": result["nested_imaginary_upper"],
        "row_origin": "full_halo_contour_evaluation",
        "error": result["error"],
        "smoke_passes": result["smoke_passes"],
    }


def augment_core(seed: dict[str, Any], geometry: dict[str, Any]) -> dict[str, Any]:
    result = dict(seed)
    result.update(geometry)
    denominator_lower = (
        float(geometry["relative_root_modulus_lower"])
        * float(geometry["selected_global_root_modulus_lower"])
        * float(geometry["collision_jacobian_modulus_lower"])
    )
    event_upper = (
        upward(float(seed["value_abs_upper"]) / denominator_lower)
        if denominator_lower > 0
        else math.inf
    )
    passes = (
        seed.get("smoke_passes") is True
        and not seed.get("error")
        and denominator_lower > 0
        and math.isfinite(event_upper)
    )
    result.update(
        {
            "event_integrand_abs_upper_without_physical_multiplier": event_upper,
            "row_origin": "seed_numerator_plus_geometry_only_enclosure",
            "error": "" if passes else str(seed.get("error") or "GEOMETRY_BLOCKED"),
            "smoke_passes": passes,
        }
    )
    return result


def reuse_full_core(seed: dict[str, Any]) -> dict[str, Any] | None:
    required_positive = (
        "event_integrand_abs_upper_without_physical_multiplier",
        "relative_root_modulus_lower",
        "selected_global_root_modulus_lower",
        "collision_jacobian_modulus_lower",
    )
    try:
        numeric_values = [float(seed[name]) for name in required_positive]
    except (KeyError, TypeError, ValueError):
        return None
    if not (
        seed.get("smoke_passes") is True
        and not seed.get("error")
        and seed.get("parent_value_is_in_nested_interval") is True
        and all(value > 0 and math.isfinite(value) for value in numeric_values)
    ):
        return None
    result = dict(seed)
    result["row_origin"] = "certified_full_core_contour_evaluation"
    return result


def status_payload(
    rows: list[dict[str, Any]], expected: int, started: float, state: str
) -> dict[str, Any]:
    elapsed = max(time.monotonic() - started, 0.0)
    failures = [row for row in rows if row.get("smoke_passes") is not True]
    event_bounds = [
        float(row.get("event_integrand_abs_upper_without_physical_multiplier", math.inf))
        for row in rows
        if math.isfinite(
            float(
                row.get(
                    "event_integrand_abs_upper_without_physical_multiplier",
                    math.inf,
                )
            )
        )
    ]
    rate = len(rows) / elapsed if elapsed > 0 else 0.0
    return {
        "state": state,
        "updated_utc": utc_now(),
        "completed_rows": len(rows),
        "expected_rows": expected,
        "remaining_rows": max(expected - len(rows), 0),
        "failure_count": len(failures),
        "elapsed_seconds": elapsed,
        "rows_per_second": rate,
        "eta_seconds": max(expected - len(rows), 0) / rate if rate > 0 else None,
        "maximum_event_integrand_abs_upper_without_physical_multiplier": (
            max(event_bounds) if event_bounds else None
        ),
        "last_row_key": list(row_key(rows[-1])) if rows else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-run-dir", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--energy-arcs", type=int, default=DEFAULT_ENERGY_ARCS)
    parser.add_argument("--global-arcs", type=int, default=DEFAULT_GLOBAL_ARCS)
    parser.add_argument("--epsilon-subdivisions", type=int, default=1)
    parser.add_argument("--status-every", type=int, default=8)
    arguments = parser.parse_args()
    seed_run = arguments.seed_run_dir.resolve()
    seed_complete = json.loads(
        (seed_run / "COMPLETE.json").read_text(encoding="utf-8")
    )
    if seed_complete.get("all_rows_pass") is not True:
        raise RuntimeError("seed numerator run is not complete and passing")
    seed_rows = read_rows(seed_run / "rows.jsonl")
    seed_lookup = {row_key(row): row for row in seed_rows}
    run_dir = arguments.run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    rows_path = run_dir / "rows.jsonl"
    rows = read_rows(rows_path)
    completed_keys = {row_key(row) for row in rows}
    boxes = M5386.contour_box_rows()
    box_keys = sorted(
        {
            (row["event_id"], int(row["epsilon_bin_index"]))
            for row in boxes
        }
    )
    expected = (
        len(box_keys)
        * arguments.epsilon_subdivisions
        * arguments.energy_arcs
        * arguments.global_arcs
    )
    status_path = run_dir / "status.json"
    complete_path = run_dir / "COMPLETE.json"
    log_path = run_dir / "log.txt"
    started = time.monotonic()
    new_rows = 0
    with rows_path.open("a", encoding="utf-8") as rows_file, log_path.open(
        "a", encoding="utf-8"
    ) as log_file:
        for event_id, epsilon_bin_index in box_keys:
            for epsilon_subdivision_index in range(
                arguments.epsilon_subdivisions
            ):
                for energy_arc_index in range(arguments.energy_arcs):
                    for global_arc_index in range(arguments.global_arcs):
                        key = (
                            event_id,
                            epsilon_bin_index,
                            epsilon_subdivision_index,
                            energy_arc_index,
                            global_arc_index,
                        )
                        if key in completed_keys:
                            continue
                        try:
                            if key in seed_lookup:
                                row = reuse_full_core(seed_lookup[key])
                                if row is None:
                                    geometry = M5386.geometric_smoke(
                                        event_id,
                                        epsilon_bin_index,
                                        energy_arc_index,
                                        epsilon_subdivision_index,
                                        arguments.epsilon_subdivisions,
                                        arguments.energy_arcs,
                                    )
                                    row = augment_core(seed_lookup[key], geometry)
                            else:
                                result = M5386.smoke(
                                    event_id,
                                    epsilon_bin_index,
                                    energy_arc_index,
                                    global_arc_index,
                                    epsilon_subdivision_index,
                                    arguments.epsilon_subdivisions,
                                    arguments.energy_arcs,
                                    arguments.global_arcs,
                                )
                                row = compact_full(result)
                        except Exception as caught:
                            row = {
                                "event_id": event_id,
                                "epsilon_bin_index": epsilon_bin_index,
                                "epsilon_subdivision_index": epsilon_subdivision_index,
                                "epsilon_subdivision_count": arguments.epsilon_subdivisions,
                                "energy_phase_arc_index": energy_arc_index,
                                "energy_phase_arc_count": arguments.energy_arcs,
                                "global_phase_arc_index": global_arc_index,
                                "global_phase_arc_count": arguments.global_arcs,
                                "value_abs_upper": math.inf,
                                "event_integrand_abs_upper_without_physical_multiplier": math.inf,
                                "relative_root_modulus_lower": 0.0,
                                "selected_global_root_modulus_lower": 0.0,
                                "collision_jacobian_modulus_lower": 0.0,
                                "collision_jacobian_chart": "ERROR",
                                "collision_jacobian_chart_denominator_lower": 0.0,
                                "collision_jacobian_recoil_derivative_upper": math.inf,
                                "minimum_denominator_lower": 0.0,
                                "energy_channel_quotient_abs_lower": 0.0,
                                "left_active_invariant_abs_lower": 0.0,
                                "parent_value_is_in_nested_interval": False,
                                "nested_interval_relative_width": math.inf,
                                "nested_real_lower": math.nan,
                                "nested_real_upper": math.nan,
                                "nested_imaginary_lower": math.nan,
                                "nested_imaginary_upper": math.nan,
                                "row_origin": "error",
                                "error": f"{type(caught).__name__}: {caught}",
                                "smoke_passes": False,
                            }
                        rows_file.write(
                            json.dumps(row, sort_keys=True, allow_nan=True) + "\n"
                        )
                        rows_file.flush()
                        rows.append(row)
                        completed_keys.add(key)
                        new_rows += 1
                        log_file.write(
                            f"{utc_now()} {key} pass={row['smoke_passes']} "
                            f"origin={row['row_origin']} error={row['error']}\n"
                        )
                        log_file.flush()
                        if new_rows % arguments.status_every == 0:
                            atomic_json(
                                status_path,
                                status_payload(rows, expected, started, "running"),
                            )
    final_status = status_payload(rows, expected, started, "complete")
    all_pass = len(rows) == expected and final_status["failure_count"] == 0
    final_status["all_rows_pass"] = all_pass
    atomic_json(status_path, final_status)
    atomic_json(
        complete_path,
        {
            "completed_utc": utc_now(),
            "all_rows_pass": all_pass,
            "completed_rows": len(rows),
            "expected_rows": expected,
            "failure_count": final_status["failure_count"],
            "seed_run_directory": str(seed_run),
        },
    )
    print(run_dir)
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
