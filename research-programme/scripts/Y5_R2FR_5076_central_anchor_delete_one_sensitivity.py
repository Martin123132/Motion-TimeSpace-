from __future__ import annotations

import csv
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5075 = POST / "scripts" / "Y5_R2FR_5075_central_anchor_estimator_recost.py"
SOURCE_5075 = POST / "source-intake" / "functional_rg" / "5075"
SOURCE = POST / "source-intake" / "functional_rg" / "5076"
RESULT_JSON = SOURCE / "central_anchor_delete_one_sensitivity.json"
PANEL_CSV = SOURCE / "delete_one_sensitivity_panels.csv"
MANIFEST_JSON = SOURCE / "locked_central_anchor_pilot_manifest.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5076_VALIDATION.csv"
MARKER = "MTS_5076_CENTRAL_ANCHOR_DELETE_ONE_SENSITIVITY"
REVISION = "joint-statistical-and-cost-delete-one-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
HIGH_UNITS = 4
EXECUTION_CAP_HOURS = 10.0
EFFICIENCY_THRESHOLD = 0.8
ANCHOR_ID = "A08"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5075 = load_module("mts_5075_for_5076", SCRIPT_5075)
M5055 = M5075.M5055


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def evaluate_allocation(
    variances: tuple[np.ndarray, np.ndarray, np.ndarray],
    margins: np.ndarray,
    high_cost: float,
    correction_cost: float,
    low_cost: float,
    low_units: int,
) -> tuple[float, float, list[float]]:
    variance_high, variance_correction, variance_low = variances
    ratio = low_units / HIGH_UNITS
    base_score = float(
        np.max(np.sqrt(variance_high * high_cost) / margins)
    )
    variance_cost = (
        variance_correction + variance_low / ratio
    ) * (correction_cost + ratio * low_cost)
    components = np.sqrt(np.maximum(variance_cost, 0.0)) / margins / base_score
    runtime = (
        HIGH_UNITS * correction_cost + low_units * low_cost
    ) / 3600.0
    return float(np.max(components)), runtime, components.tolist()


def main() -> None:
    recost_path = SOURCE_5075 / "central_anchor_estimator_recost.json"
    event_cost_path = SOURCE_5075 / "central_anchor_event_costs.csv"
    required = [SCRIPT_5075, recost_path, event_cost_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    recost = json.loads(recost_path.read_text(encoding="utf-8"))
    event_costs = {
        row["event_id"]: row
        for row in csv.DictReader(event_cost_path.open(encoding="utf-8"))
    }
    M5055.M5049.configure_modules()
    M5055.M5044.M5043 = M5055.M5049.M5043
    config = M5055.M5049.M5043.load_config()
    event_rows = M5055.M5044.event_dataset(config)
    event_ids = [str(row["event_id"]) for row in event_rows]
    seeds = sorted({int(row["seed"]) for row in event_rows})
    shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
    projector = np.eye(5) - np.outer(shape, shape) / float(shape @ shape)
    high_complex_rows = []
    correction_rows = []
    low_rows = []
    for row in event_rows:
        event_id = str(row["event_id"])
        e020 = {
            base_id: M5055.M5049.M5043.complex_value(
                M5055.M5049.M5043.primary_job("E020", event_id, base_id)[
                    "normalized_direct_D_hhh_over_G3"
                ]
            )
            for base_id in row["coarse"]
        }
        high_raw = 2.0 * M5055.M5054.raw_cyclic(
            config, e020
        ) - M5055.M5054.raw_cyclic(config, row["full"])
        low_raw = M5055.M5054.raw_cyclic(config, row["coarse"])
        high = projector @ high_raw
        correction = projector @ (high_raw - low_raw)
        low = projector @ low_raw
        high_complex_rows.append(high)
        correction_rows.append(
            np.concatenate((correction.real, high.imag))
        )
        low_rows.append(
            np.concatenate((low.real, np.zeros(5, dtype=float)))
        )
    high_channels = M5055.M5049.M5043.channel_matrix(
        np.stack(high_complex_rows)
    )
    correction_channels = np.stack(correction_rows)
    low_channels = np.stack(low_rows)
    sample_indices = np.asarray(
        [int(row["sample_index"]) for row in event_rows]
    )
    real_margins = np.asarray(
        [
            float(row["target_equivalence_margin"])
            for row in config["target_precision_budgets"]
        ]
    )
    margins = np.concatenate((real_margins, real_margins))
    panels = [("full", "none", set())]
    panels.extend(
        (f"delete_event_{event_id}", "event", {event_id})
        for event_id in event_ids
    )
    panels.extend(
        (
            f"delete_seed_{seed}",
            "seed",
            {
                str(row["event_id"])
                for row in event_rows
                if int(row["seed"]) == seed
            },
        )
        for seed in seeds
    )
    panel_data = []
    for panel_id, deletion_type, deleted in panels:
        retained = np.asarray(
            [event_id not in deleted for event_id in event_ids]
        )
        stratum_variances = []
        for sample_index in (0, 1):
            selected = retained & (sample_indices == sample_index)
            if int(np.sum(selected)) < 2:
                raise RuntimeError(
                    f"panel {panel_id} leaves fewer than two rows in stratum {sample_index}"
                )
            stratum_variances.append(
                tuple(
                    np.var(values[selected], axis=0, ddof=1)
                    for values in (
                        high_channels,
                        correction_channels,
                        low_channels,
                    )
                )
            )
        conservative_variances = tuple(
            np.maximum(
                stratum_variances[0][index],
                stratum_variances[1][index],
            )
            for index in range(3)
        )
        retained_costs = [
            event_costs[event_id]
            for event_id in event_ids
            if event_id not in deleted
        ]
        panel_high_cost = float(
            np.mean(
                [
                    float(row["projected_high_primary_seconds"])
                    for row in retained_costs
                ]
            )
        )
        panel_correction_cost = float(
            np.mean(
                [
                    float(row["projected_paired_correction_seconds"])
                    for row in retained_costs
                ]
            )
        )
        panel_low_cost = float(
            np.mean(
                [
                    float(row["projected_low_only_seconds"])
                    for row in retained_costs
                ]
            )
        )
        panel_data.append(
            {
                "panel_id": panel_id,
                "deletion_type": deletion_type,
                "deleted_ids": sorted(deleted),
                "retained_event_count": int(np.sum(retained)),
                "variances": conservative_variances,
                "high_cost": panel_high_cost,
                "correction_cost": panel_correction_cost,
                "low_cost": panel_low_cost,
            }
        )
    fixed_high_cost = float(recost["mean_projected_high_primary_seconds"])
    fixed_correction_cost = float(
        recost["mean_projected_paired_correction_seconds"]
    )
    fixed_low_cost = float(recost["mean_projected_low_only_seconds"])
    robust_fixed_cost = None
    robust_joint = None
    for low_units in range(1, 513):
        fixed_values = [
            evaluate_allocation(
                panel["variances"],
                margins,
                fixed_high_cost,
                fixed_correction_cost,
                fixed_low_cost,
                low_units,
            )
            for panel in panel_data
        ]
        joint_values = [
            evaluate_allocation(
                panel["variances"],
                margins,
                float(panel["high_cost"]),
                float(panel["correction_cost"]),
                float(panel["low_cost"]),
                low_units,
            )
            for panel in panel_data
        ]
        if robust_fixed_cost is None and all(
            score < EFFICIENCY_THRESHOLD and runtime <= EXECUTION_CAP_HOURS
            for score, runtime, _ in fixed_values
        ):
            robust_fixed_cost = {
                "low_units": low_units,
                "maximum_score_ratio": max(value[0] for value in fixed_values),
                "maximum_runtime_hours": max(value[1] for value in fixed_values),
            }
        if robust_joint is None and all(
            score < EFFICIENCY_THRESHOLD and runtime <= EXECUTION_CAP_HOURS
            for score, runtime, _ in joint_values
        ):
            robust_joint = {
                "low_units": low_units,
                "maximum_score_ratio": max(value[0] for value in joint_values),
                "maximum_runtime_hours": max(value[1] for value in joint_values),
            }
        if robust_fixed_cost is not None and robust_joint is not None:
            break
    locked_low_units = (
        int(robust_joint["low_units"]) if robust_joint is not None else None
    )
    output_rows = []
    if locked_low_units is not None:
        for panel in panel_data:
            fixed_score, fixed_runtime, _ = evaluate_allocation(
                panel["variances"],
                margins,
                fixed_high_cost,
                fixed_correction_cost,
                fixed_low_cost,
                locked_low_units,
            )
            joint_score, joint_runtime, components = evaluate_allocation(
                panel["variances"],
                margins,
                float(panel["high_cost"]),
                float(panel["correction_cost"]),
                float(panel["low_cost"]),
                locked_low_units,
            )
            output_rows.append(
                {
                    "panel_id": panel["panel_id"],
                    "deletion_type": panel["deletion_type"],
                    "deleted_ids": ";".join(panel["deleted_ids"]),
                    "retained_event_count": panel["retained_event_count"],
                    "locked_low_units": locked_low_units,
                    "fixed_cost_score_ratio": fixed_score,
                    "fixed_cost_runtime_hours": fixed_runtime,
                    "joint_score_ratio": joint_score,
                    "joint_runtime_hours": joint_runtime,
                    "worst_component_index": int(np.argmax(components)),
                    "passes_joint_gate": joint_score < EFFICIENCY_THRESHOLD
                    and joint_runtime <= EXECUTION_CAP_HOURS,
                }
            )
    upstream_gates = bool(recost["bidirectional_chain_gate_inherited"]) and bool(
        recost["kernel_heldout_gate_inherited"]
    )
    statistically_locked = (
        robust_fixed_cost is not None
        and robust_joint is not None
        and len(output_rows) == 13
        and all(row["passes_joint_gate"] for row in output_rows)
    )
    manifest = {
        "checkpoint_marker": MARKER,
        "status": "LOCKED_NOT_EXECUTABLE",
        "design": "single_componentwise_conservative",
        "high_units": HIGH_UNITS,
        "low_units": locked_low_units,
        "anchor_argument_id": ANCHOR_ID,
        "argument_topology_rule": "bidirectional canonical path composition from A08",
        "epsilon_topology_rule": "certified E040-to-E020 vertical composition",
        "quadrature_breakpoint_rule": "near-path collision roots only",
        "fresh_high_scramble_seeds": [507601, 507602, 507603, 507604],
        "fresh_high_sample_index": 0,
        "fresh_low_scramble_seeds": [
            507610 + index for index in range(1, (locked_low_units or 0) + 1)
        ],
        "execution_cap_hours": EXECUTION_CAP_HOURS,
        "maximum_delete_one_projected_runtime_hours": robust_joint[
            "maximum_runtime_hours"
        ]
        if robust_joint
        else None,
        "maximum_delete_one_score_ratio": robust_joint["maximum_score_ratio"]
        if robust_joint
        else None,
        "statistical_design_locked": statistically_locked,
        "runner_integration_complete": False,
        "pilot_execution_authorized": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST_JSON, manifest)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "panel_count": len(panel_data),
        "delete_one_event_panel_count": sum(
            panel["deletion_type"] == "event" for panel in panel_data
        ),
        "delete_one_seed_panel_count": sum(
            panel["deletion_type"] == "seed" for panel in panel_data
        ),
        "robust_fixed_cost_allocation": robust_fixed_cost,
        "robust_joint_statistical_cost_allocation": robust_joint,
        "statistical_design_locked": statistically_locked,
        "locked_manifest_path": str(MANIFEST_JSON),
        "upstream_gates_inherited": upstream_gates,
        "pilot_execution_authorized": False,
        "next_required_gate": "integrate the A08 bidirectional constructor and history-invariant quadrature behind an opt-in pilot runner, then dry-run the locked manifest",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    SOURCE.mkdir(parents=True, exist_ok=True)
    with PANEL_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    checks = [
        ("source_paths_exist", all(path.exists() for path in required), "5075 recost and event costs exist"),
        ("panel_matrix_complete", len(panel_data) == 13, f"panels={len(panel_data)}"),
        ("delete_one_event_complete", result["delete_one_event_panel_count"] == 8, f"panels={result['delete_one_event_panel_count']}"),
        ("delete_one_seed_complete", result["delete_one_seed_panel_count"] == 4, f"panels={result['delete_one_seed_panel_count']}"),
        ("fixed_cost_robust_allocation", robust_fixed_cost is not None, str(robust_fixed_cost)),
        ("joint_robust_allocation", robust_joint is not None, str(robust_joint)),
        ("all_locked_panels_pass", len(output_rows) == 13 and all(row["passes_joint_gate"] for row in output_rows), f"passed={sum(bool(row['passes_joint_gate']) for row in output_rows)}/{len(output_rows)}"),
        ("upstream_gates_inherited", upstream_gates, "bidirectional topology and heldout kernel gates pass"),
        ("statistical_design_locked", statistically_locked, f"low units={locked_low_units}"),
        ("execution_still_blocked", not manifest["runner_integration_complete"] and not manifest["pilot_execution_authorized"], "manifest cannot execute before runner integration and dry-run"),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "jackknife/cost robustness is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5076_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "check_count": len(checks),
                "failed": failed,
                "passed": not failed,
                "output": str(RESULT_JSON),
            },
            indent=2,
        )
    )
    if failed:
        raise RuntimeError(f"checkpoint 5076 validation failed: {failed}")


if __name__ == "__main__":
    main()
