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
SCRIPT_5386 = (
    POST
    / "scripts"
    / "Y5_R2FR_5386_D4_nested_contour_integrand_enclosure.py"
)
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


M5386 = load_module("mts_5386_for_uniform_bound", SCRIPT_5386)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def row_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row["event_id"],
        int(row["epsilon_bin_index"]),
        int(row["epsilon_subdivision_index"]),
        int(row["energy_phase_arc_index"]),
        int(row["global_phase_arc_index"]),
    )


def read_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def compact_row(result: dict[str, Any]) -> dict[str, Any]:
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
        "collision_root_difference_modulus_upper": result[
            "collision_root_difference_modulus_upper"
        ],
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
        "error": result["error"],
        "smoke_passes": result["smoke_passes"],
    }


def status_payload(
    rows: list[dict[str, Any]],
    expected_rows: int,
    started_at: float,
    state: str,
) -> dict[str, Any]:
    elapsed = max(time.monotonic() - started_at, 0.0)
    completed = len(rows)
    rate = completed / elapsed if elapsed > 0 else 0.0
    remaining = max(expected_rows - completed, 0)
    failures = [
        row
        for row in rows
        if row.get("error") or row.get("smoke_passes") is not True
    ]
    finite_upper_bounds = [
        float(row["value_abs_upper"])
        for row in rows
        if math.isfinite(float(row["value_abs_upper"]))
    ]
    finite_event_integrand_bounds = [
        float(row["event_integrand_abs_upper_without_physical_multiplier"])
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
    positive_denominators = [
        float(row["minimum_denominator_lower"])
        for row in rows
        if float(row["minimum_denominator_lower"]) > 0
    ]
    geometric_minima = {
        name: min(
            (
                float(row.get(name, 0.0))
                for row in rows
                if float(row.get(name, 0.0)) > 0
            ),
            default=None,
        )
        for name in (
            "relative_root_modulus_lower",
            "selected_global_root_modulus_lower",
            "collision_jacobian_modulus_lower",
        )
    }
    return {
        "state": state,
        "updated_utc": utc_now(),
        "completed_rows": completed,
        "expected_rows": expected_rows,
        "remaining_rows": remaining,
        "failure_count": len(failures),
        "elapsed_seconds": elapsed,
        "rows_per_second": rate,
        "eta_seconds": remaining / rate if rate > 0 else None,
        "maximum_value_abs_upper": (
            max(finite_upper_bounds) if finite_upper_bounds else None
        ),
        "maximum_event_integrand_abs_upper_without_physical_multiplier": (
            max(finite_event_integrand_bounds)
            if finite_event_integrand_bounds
            else None
        ),
        "minimum_denominator_lower": (
            min(positive_denominators) if positive_denominators else None
        ),
        "geometric_factor_minima": geometric_minima,
        "last_row_key": list(row_key(rows[-1])) if rows else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--energy-arcs", type=int, default=DEFAULT_ENERGY_ARCS)
    parser.add_argument("--global-arcs", type=int, default=DEFAULT_GLOBAL_ARCS)
    parser.add_argument("--epsilon-subdivisions", type=int, default=1)
    parser.add_argument("--max-new-rows", type=int, default=0)
    parser.add_argument("--status-every", type=int, default=8)
    arguments = parser.parse_args()
    if arguments.energy_arcs < 1 or arguments.global_arcs < 1:
        parser.error("phase arc counts must be positive")
    if arguments.epsilon_subdivisions < 1:
        parser.error("epsilon subdivision count must be positive")
    run_dir = arguments.run_dir
    if run_dir is None:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir = POST / "runs" / f"{stamp}-5386-uniform-H3-contour-bound"
    run_dir = run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    rows_path = run_dir / "rows.jsonl"
    status_path = run_dir / "status.json"
    log_path = run_dir / "log.txt"
    complete_path = run_dir / "COMPLETE.json"
    boxes = M5386.contour_box_rows()
    box_keys = sorted(
        {
            (row["event_id"], int(row["epsilon_bin_index"]))
            for row in boxes
        }
    )
    expected_rows = (
        len(box_keys)
        * arguments.epsilon_subdivisions
        * arguments.energy_arcs
        * arguments.global_arcs
    )
    rows = read_rows(rows_path)
    completed_keys = {row_key(row) for row in rows}
    started_at = time.monotonic()
    new_rows = 0
    with log_path.open("a", encoding="utf-8") as log_file, rows_path.open(
        "a", encoding="utf-8"
    ) as rows_file:
        log_file.write(
            f"{utc_now()} start expected={expected_rows} existing={len(rows)} "
            f"energy_arcs={arguments.energy_arcs} "
            f"global_arcs={arguments.global_arcs} "
            f"epsilon_subdivisions={arguments.epsilon_subdivisions}\n"
        )
        log_file.flush()
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
                            row = compact_row(result)
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
                                "collision_root_difference_modulus_upper": math.inf,
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
                            f"upper={row['value_abs_upper']} "
                            f"denominator={row['minimum_denominator_lower']} "
                            f"error={row['error']}\n"
                        )
                        log_file.flush()
                        if new_rows % arguments.status_every == 0:
                            atomic_write_json(
                                status_path,
                                status_payload(
                                    rows, expected_rows, started_at, "running"
                                ),
                            )
                        if (
                            arguments.max_new_rows > 0
                            and new_rows >= arguments.max_new_rows
                        ):
                            atomic_write_json(
                                status_path,
                                status_payload(
                                    rows,
                                    expected_rows,
                                    started_at,
                                    "partial",
                                ),
                            )
                            print(run_dir)
                            return 0
    final_status = status_payload(
        rows,
        expected_rows,
        started_at,
        "complete",
    )
    all_pass = (
        len(rows) == expected_rows
        and final_status["failure_count"] == 0
    )
    final_status["all_rows_pass"] = all_pass
    atomic_write_json(status_path, final_status)
    atomic_write_json(
        complete_path,
        {
            "completed_utc": utc_now(),
            "all_rows_pass": all_pass,
            "completed_rows": len(rows),
            "expected_rows": expected_rows,
            "failure_count": final_status["failure_count"],
        },
    )
    print(run_dir)
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
