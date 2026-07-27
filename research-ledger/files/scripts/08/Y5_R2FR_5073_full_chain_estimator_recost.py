from __future__ import annotations

import csv
import importlib.util
import json
import os
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5055 = POST / "scripts" / "Y5_R2FR_5055_variance_cost_sample_unit_repair.py"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE_5055 = POST / "source-intake" / "functional_rg" / "5055"
SOURCE_5065 = POST / "source-intake" / "functional_rg" / "5065"
SOURCE_5069 = POST / "source-intake" / "functional_rg" / "5069"
SOURCE_5070 = POST / "source-intake" / "functional_rg" / "5070"
SOURCE_5072 = POST / "source-intake" / "functional_rg" / "5072"
SOURCE = POST / "source-intake" / "functional_rg" / "5073"
RESULT_JSON = SOURCE / "full_chain_estimator_recost.json"
EVENT_CSV = SOURCE / "full_chain_event_costs.csv"
DESIGN_CSV = SOURCE / "full_chain_designs.csv"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5073_VALIDATION.csv"
MARKER = "MTS_5073_FULL_CHAIN_ESTIMATOR_RECOST"
REVISION = "eight-anchor-all-argument-all-epsilon-transport-cost-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
CONSTRUCTOR_ALLOWANCE_SECONDS = 0.1


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5055 = load_module("mts_5055_for_5073", SCRIPT_5055)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def main() -> None:
    cost_rows_path = SOURCE_5053 / "high_low_cost_rows.csv"
    event_rows_path = SOURCE_5053 / "high_low_event_costs.csv"
    source_cost_path = SOURCE_5053 / "high_low_cost_provenance_and_reuse_audit.json"
    source_design_path = SOURCE_5055 / "variance_cost_sample_unit_repair.json"
    historical_constructor_path = SOURCE_5065 / "argument_chain_event_costs.csv"
    epsilon_rows_path = SOURCE_5069 / "winding_composition_rows.csv"
    composition_result_path = SOURCE_5069 / "signed_segment_winding_composition_law.json"
    chain_rows_path = SOURCE_5070 / "canonical_argument_chain_rows.csv"
    chain_result_path = SOURCE_5070 / "canonical_argument_chain_constructor_gate.json"
    kernel_result_path = SOURCE_5072 / "history_invariant_kernel_heldout_matrix.json"
    required = [
        SCRIPT_5055,
        cost_rows_path,
        event_rows_path,
        source_cost_path,
        source_design_path,
        historical_constructor_path,
        epsilon_rows_path,
        composition_result_path,
        chain_rows_path,
        chain_result_path,
        kernel_result_path,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    cost_rows = list(csv.DictReader(cost_rows_path.open(encoding="utf-8")))
    source_events = {
        row["event_id"]: row
        for row in csv.DictReader(event_rows_path.open(encoding="utf-8"))
    }
    chain_rows = list(csv.DictReader(chain_rows_path.open(encoding="utf-8")))
    epsilon_rows = [
        row
        for row in csv.DictReader(epsilon_rows_path.open(encoding="utf-8"))
        if row["suite"] == "E040_TO_E020"
    ]
    historical_constructor_rows = list(
        csv.DictReader(historical_constructor_path.open(encoding="utf-8"))
    )
    historical_constructor_seconds = sum(
        float(row["constructor_seconds"]) for row in historical_constructor_rows
    )
    historical_constructor_edges = sum(
        int(row["transport_edge_count"]) for row in historical_constructor_rows
    )
    historical_constructor_mean = (
        historical_constructor_seconds / historical_constructor_edges
    )
    constructor_allowance_multiple = (
        CONSTRUCTOR_ALLOWANCE_SECONDS / historical_constructor_mean
    )
    source_cost = json.loads(source_cost_path.read_text(encoding="utf-8"))
    source_design = json.loads(source_design_path.read_text(encoding="utf-8"))
    composition_result = json.loads(
        composition_result_path.read_text(encoding="utf-8")
    )
    chain_result = json.loads(chain_result_path.read_text(encoding="utf-8"))
    kernel_result = json.loads(kernel_result_path.read_text(encoding="utf-8"))
    event_ids = sorted(source_events)
    event_rows = []
    for event_id in event_ids:
        event_cost_rows = [row for row in cost_rows if row["event_id"] == event_id]
        source_event = source_events[event_id]
        anchor_measured = float(
            next(
                row
                for row in event_cost_rows
                if row["base_argument_id"] == "A00"
            )["e040_topology_runtime_seconds"]
        )
        positive_e040 = [
            float(row["e040_topology_runtime_seconds"])
            for row in event_cost_rows
            if float(row["e040_topology_runtime_seconds"]) > 0.0
        ]
        anchor_floor = float(np.median(positive_e040))
        charged_anchor = max(anchor_measured, anchor_floor)
        argument_certificate_seconds = sum(
            float(row["certificate_runtime_seconds"])
            for row in chain_rows
            if row["event_id"] == event_id
        )
        epsilon_certificate_seconds = sum(
            float(row["certificate_runtime_seconds"])
            for row in epsilon_rows
            if row["event_id"] == event_id
        )
        e040_constructor_allowance = 14 * CONSTRUCTOR_ALLOWANCE_SECONDS
        e020_constructor_allowance = 15 * CONSTRUCTOR_ALLOWANCE_SECONDS
        projected_e040_topology = (
            charged_anchor
            + argument_certificate_seconds
            + e040_constructor_allowance
        )
        projected_e020_topology = (
            epsilon_certificate_seconds + e020_constructor_allowance
        )
        projected_high_topology = projected_e040_topology + projected_e020_topology
        high_kernel = float(source_event["high_primary_kernel_cost_seconds"])
        low_kernel = float(source_event["low_only_kernel_cost_seconds"])
        paired_low_kernel = float(source_event["paired_low_kernel_cost_seconds"])
        projected_high = projected_high_topology + high_kernel
        projected_correction = projected_high + paired_low_kernel
        projected_low = projected_e040_topology + low_kernel
        event_rows.append(
            {
                "event_id": event_id,
                "measured_a00_anchor_seconds": anchor_measured,
                "positive_event_median_anchor_floor_seconds": anchor_floor,
                "charged_anchor_seconds": charged_anchor,
                "argument_certificate_seconds": argument_certificate_seconds,
                "epsilon_certificate_seconds": epsilon_certificate_seconds,
                "e040_constructor_allowance_seconds": e040_constructor_allowance,
                "e020_constructor_allowance_seconds": e020_constructor_allowance,
                "projected_e040_topology_seconds": projected_e040_topology,
                "projected_e020_topology_seconds": projected_e020_topology,
                "projected_high_topology_seconds": projected_high_topology,
                "current_high_primary_seconds": float(
                    source_event["high_primary_cost_seconds"]
                ),
                "projected_high_primary_seconds": projected_high,
                "current_paired_correction_seconds": float(
                    source_event["paired_high_correction_cost_seconds"]
                ),
                "projected_paired_correction_seconds": projected_correction,
                "current_low_only_seconds": float(
                    source_event["low_only_total_cost_seconds"]
                ),
                "projected_low_only_seconds": projected_low,
            }
        )
    current_high = float(source_cost["mean_high_primary_event_cost_seconds"])
    current_correction = float(
        source_cost["mean_paired_high_correction_event_cost_seconds"]
    )
    current_low = float(source_cost["mean_low_only_total_event_cost_seconds"])
    projected_high = float(
        np.mean([row["projected_high_primary_seconds"] for row in event_rows])
    )
    projected_correction = float(
        np.mean(
            [row["projected_paired_correction_seconds"] for row in event_rows]
        )
    )
    projected_low = float(
        np.mean([row["projected_low_only_seconds"] for row in event_rows])
    )
    M5055.M5049.configure_modules()
    config = M5055.M5049.M5043.load_config()
    real_margins = np.asarray(
        [
            float(row["target_equivalence_margin"])
            for row in config["target_precision_budgets"]
        ]
    )
    margins = np.concatenate((real_margins, real_margins))
    designs = []
    reproduction_differences = []
    for source_row in source_design["designs"]:
        variance_high = np.asarray(source_row["variance_high"], dtype=float)
        variance_correction = np.asarray(
            source_row["variance_correction"], dtype=float
        )
        variance_low = np.asarray(
            source_row["variance_low_contribution"], dtype=float
        )
        reproduced = M5055.design_metrics(
            str(source_row["design"]),
            str(source_row["evidence_role"]),
            int(source_row["events_per_variance_unit"]),
            variance_high,
            variance_correction,
            variance_low,
            margins,
            current_high,
            current_correction,
            current_low,
        )
        adjusted = M5055.design_metrics(
            str(source_row["design"]),
            str(source_row["evidence_role"]),
            int(source_row["events_per_variance_unit"]),
            variance_high,
            variance_correction,
            variance_low,
            margins,
            projected_high,
            projected_correction,
            projected_low,
        )
        reproduction_differences.append(
            abs(
                float(reproduced["continuous_optimal_score_ratio"])
                - float(source_row["continuous_optimal_score_ratio"])
            )
        )
        designs.append(adjusted)
    admissible = [
        row
        for row in designs
        if row["evidence_role"]
        in {"admissible paired design", "admissible conservative envelope"}
    ]
    sub_cap = [
        row for row in admissible if row["sub_10_hour_efficiency_candidate"]
    ]
    conservative = next(
        row
        for row in designs
        if row["design"] == "single_componentwise_conservative"
    )
    paired = next(
        row for row in designs if row["design"] == "paired_nested_two_event"
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_count": len(event_rows),
        "full_e040_anchor_count": 8,
        "constructed_e040_topology_count": 112,
        "constructed_e020_topology_count": 120,
        "constructor_allowance_seconds_per_artifact": CONSTRUCTOR_ALLOWANCE_SECONDS,
        "historical_constructor_mean_seconds_per_artifact": historical_constructor_mean,
        "constructor_allowance_multiple": constructor_allowance_multiple,
        "mean_current_high_primary_seconds": current_high,
        "mean_projected_high_primary_seconds": projected_high,
        "mean_current_paired_correction_seconds": current_correction,
        "mean_projected_paired_correction_seconds": projected_correction,
        "mean_current_low_only_seconds": current_low,
        "mean_projected_low_only_seconds": projected_low,
        "high_primary_cost_reduction_fraction": (current_high - projected_high)
        / current_high,
        "paired_correction_cost_reduction_fraction": (
            current_correction - projected_correction
        )
        / current_correction,
        "low_only_cost_reduction_fraction": (current_low - projected_low)
        / current_low,
        "adjusted_designs": designs,
        "paired_minimum_efficiency_runtime_hours": paired[
            "minimum_runtime_integer_passing_efficiency"
        ]["runtime_hours"],
        "conservative_minimum_efficiency": conservative[
            "minimum_runtime_integer_passing_efficiency"
        ],
        "conservative_best_under_cap": conservative["best_integer_under_cap"],
        "sub_10_hour_admissible_candidate_count": len(sub_cap),
        "composition_gate_inherited": bool(
            composition_result["signed_winding_composition_gate_passed"]
        ),
        "recursive_chain_gate_inherited": bool(
            chain_result["canonical_argument_chain_gate_passed"]
        ),
        "kernel_heldout_gate_inherited": bool(
            kernel_result["history_invariant_kernel_heldout_gate_passed"]
        ),
        "source_reproduction_maximum_score_difference": max(
            reproduction_differences
        ),
        "retrospective_cost_projection_only": True,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "lock the bounded conservative pilot manifest and run delete-one-event cost sensitivity before launch",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    SOURCE.mkdir(parents=True, exist_ok=True)
    with EVENT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(event_rows[0]))
        writer.writeheader()
        writer.writerows(event_rows)
    design_rows = []
    for row in designs:
        under = row["best_integer_under_cap"]
        efficient = row["minimum_runtime_integer_passing_efficiency"]
        design_rows.append(
            {
                "design": row["design"],
                "evidence_role": row["evidence_role"],
                "continuous_optimal_score_ratio": row[
                    "continuous_optimal_score_ratio"
                ],
                "best_under_cap_score_ratio": under["score_ratio"]
                if under
                else None,
                "best_under_cap_runtime_hours": under["runtime_hours"]
                if under
                else None,
                "best_under_cap_low_units": under["low_units"]
                if under
                else None,
                "minimum_efficiency_runtime_hours": efficient["runtime_hours"],
                "minimum_efficiency_low_units": efficient["low_units"],
                "sub_10_hour_efficiency_candidate": row[
                    "sub_10_hour_efficiency_candidate"
                ],
            }
        )
    with DESIGN_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(design_rows[0]))
        writer.writeheader()
        writer.writerows(design_rows)
    gates_inherited = (
        result["composition_gate_inherited"]
        and result["recursive_chain_gate_inherited"]
        and result["kernel_heldout_gate_inherited"]
    )
    checks = [
        ("source_paths_exist", all(path.exists() for path in required), "5053, 5055, 5065, 5069, 5070, and 5072 inputs exist"),
        ("event_matrix_complete", len(event_rows) == 8, f"events={len(event_rows)}"),
        ("source_design_reproduced", max(reproduction_differences) < 1.0e-9, f"maximum score difference={max(reproduction_differences)}"),
        ("transport_and_kernel_gates_inherited", gates_inherited, "composition, recursive chain, and heldout kernel gates pass"),
        ("nonzero_anchor_floor", all(float(row["charged_anchor_seconds"]) > 0.0 for row in event_rows), "every event charges a positive full anchor"),
        ("conservative_constructor_allowance", constructor_allowance_multiple >= 20.0, f"allowance multiple={constructor_allowance_multiple}"),
        ("positive_projected_costs", min(min(row["projected_high_primary_seconds"], row["projected_paired_correction_seconds"], row["projected_low_only_seconds"]) for row in event_rows) > 0.0, "all projected event costs remain positive"),
        ("all_mean_costs_reduced", projected_high < current_high and projected_correction < current_correction and projected_low < current_low, f"high={projected_high}; correction={projected_correction}; low={projected_low}"),
        ("sample_units_preserved", next(row["events_per_variance_unit"] for row in designs if row["design"] == "paired_nested_two_event") == 2, "paired design still charges two events per variance unit"),
        ("sub_ten_hour_admissible_candidate", len(sub_cap) >= 1 and bool(conservative["sub_10_hour_efficiency_candidate"]), f"admissible candidates={len(sub_cap)}; conservative runtime={conservative['minimum_runtime_integer_passing_efficiency']['runtime_hours']}"),
        ("no_fresh_execution", not result["fresh_kernel_execution_authorized"], "recost launches no pilot"),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", result["retrospective_cost_projection_only"] and not result["valid_for_full_MTS_claim"], "cost feasibility is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5073_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5073 validation failed: {failed}")


if __name__ == "__main__":
    main()
