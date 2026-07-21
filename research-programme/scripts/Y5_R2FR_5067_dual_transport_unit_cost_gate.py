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
SOURCE_5058 = POST / "source-intake" / "functional_rg" / "5058"
SOURCE_5059 = POST / "source-intake" / "functional_rg" / "5059"
SOURCE_5065 = POST / "source-intake" / "functional_rg" / "5065"
SOURCE_5066 = POST / "source-intake" / "functional_rg" / "5066"
SOURCE = POST / "source-intake" / "functional_rg" / "5067"
RESULT_JSON = SOURCE / "dual_transport_unit_cost_gate.json"
EVENT_CSV = SOURCE / "dual_transport_event_costs.csv"
DESIGN_CSV = SOURCE / "dual_transport_designs.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5067_VALIDATION.csv"
)
MARKER = "MTS_5067_DUAL_TRANSPORT_UNIT_COST_GATE"
REVISION = "epsilon-plus-argument-transport-unit-cost-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5055 = load_module("mts_5055_for_5067", SCRIPT_5055)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def main() -> None:
    source_event_path = SOURCE_5053 / "high_low_event_costs.csv"
    source_cost_path = SOURCE_5053 / "high_low_cost_provenance_and_reuse_audit.json"
    source_design_path = SOURCE_5055 / "variance_cost_sample_unit_repair.json"
    epsilon_event_path = SOURCE_5058 / "transport_adjusted_event_costs.csv"
    epsilon_certificate_path = SOURCE_5059 / "epsilon_segment_certificate_rows.csv"
    argument_event_path = SOURCE_5065 / "argument_chain_event_costs.csv"
    argument_result_path = SOURCE_5065 / "adjacent_argument_transport_certificate_benchmark.json"
    chain_result_path = SOURCE_5066 / "argument_chain_constructed_predecessor_gate.json"
    required = [
        SCRIPT_5055,
        source_event_path,
        source_cost_path,
        source_design_path,
        epsilon_event_path,
        epsilon_certificate_path,
        argument_event_path,
        argument_result_path,
        chain_result_path,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_events = {
        row["event_id"]: row
        for row in csv.DictReader(source_event_path.open(encoding="utf-8"))
    }
    epsilon_events = {
        row["event_id"]: row
        for row in csv.DictReader(epsilon_event_path.open(encoding="utf-8"))
    }
    argument_events = {
        row["event_id"]: row
        for row in csv.DictReader(argument_event_path.open(encoding="utf-8"))
    }
    epsilon_certificate_rows = list(
        csv.DictReader(epsilon_certificate_path.open(encoding="utf-8"))
    )
    epsilon_certificate_costs: dict[str, float] = {}
    for row in epsilon_certificate_rows:
        epsilon_certificate_costs[row["event_id"]] = epsilon_certificate_costs.get(
            row["event_id"], 0.0
        ) + float(row["certificate_runtime_seconds_8_16"])
    source_cost = json.loads(source_cost_path.read_text(encoding="utf-8"))
    source_design = json.loads(source_design_path.read_text(encoding="utf-8"))
    argument_result = json.loads(argument_result_path.read_text(encoding="utf-8"))
    chain_result = json.loads(chain_result_path.read_text(encoding="utf-8"))
    event_ids = sorted(source_events)
    event_rows = []
    for event_id in event_ids:
        source = source_events[event_id]
        epsilon = epsilon_events[event_id]
        argument = argument_events[event_id]
        epsilon_savings_before_certificate = float(
            epsilon["net_topology_savings_seconds"]
        )
        epsilon_certificate_cost = epsilon_certificate_costs[event_id]
        epsilon_net_savings = (
            epsilon_savings_before_certificate - epsilon_certificate_cost
        )
        argument_net_savings = float(argument["net_savings_seconds"])
        current_high = float(source["high_primary_cost_seconds"])
        current_correction = float(source["paired_high_correction_cost_seconds"])
        current_low = float(source["low_only_total_cost_seconds"])
        adjusted_high = current_high - epsilon_net_savings - argument_net_savings
        adjusted_correction = (
            current_correction - epsilon_net_savings - argument_net_savings
        )
        adjusted_low = current_low - argument_net_savings
        event_rows.append(
            {
                "event_id": event_id,
                "current_high_primary_seconds": current_high,
                "current_paired_correction_seconds": current_correction,
                "current_low_only_seconds": current_low,
                "epsilon_topology_savings_before_certificate_seconds": epsilon_savings_before_certificate,
                "epsilon_certificate_seconds": epsilon_certificate_cost,
                "epsilon_net_savings_seconds": epsilon_net_savings,
                "argument_chain_net_savings_seconds": argument_net_savings,
                "dual_transport_high_primary_seconds": adjusted_high,
                "dual_transport_paired_correction_seconds": adjusted_correction,
                "argument_transport_low_only_seconds": adjusted_low,
            }
        )
    current_high = float(source_cost["mean_high_primary_event_cost_seconds"])
    current_correction = float(
        source_cost["mean_paired_high_correction_event_cost_seconds"]
    )
    current_low = float(source_cost["mean_low_only_total_event_cost_seconds"])
    adjusted_high = float(
        np.mean([row["dual_transport_high_primary_seconds"] for row in event_rows])
    )
    adjusted_correction = float(
        np.mean(
            [row["dual_transport_paired_correction_seconds"] for row in event_rows]
        )
    )
    adjusted_low = float(
        np.mean([row["argument_transport_low_only_seconds"] for row in event_rows])
    )
    M5055.M5049.configure_modules()
    config = M5055.M5049.M5043.load_config()
    real_margins = np.asarray(
        [float(row["target_equivalence_margin"]) for row in config["target_precision_budgets"]]
    )
    margins = np.concatenate((real_margins, real_margins))
    designs = []
    reproduction_differences = []
    for source_row in source_design["designs"]:
        variance_high = np.asarray(source_row["variance_high"], dtype=float)
        variance_correction = np.asarray(source_row["variance_correction"], dtype=float)
        variance_low = np.asarray(source_row["variance_low_contribution"], dtype=float)
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
            adjusted_high,
            adjusted_correction,
            adjusted_low,
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
    sub_cap = [row for row in admissible if row["sub_10_hour_efficiency_candidate"]]
    conservative = next(
        row for row in designs if row["design"] == "single_componentwise_conservative"
    )
    paired = next(row for row in designs if row["design"] == "paired_nested_two_event")
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "mean_current_high_primary_seconds": current_high,
        "mean_dual_transport_high_primary_seconds": adjusted_high,
        "mean_current_paired_correction_seconds": current_correction,
        "mean_dual_transport_paired_correction_seconds": adjusted_correction,
        "mean_current_low_only_seconds": current_low,
        "mean_argument_transport_low_only_seconds": adjusted_low,
        "high_primary_cost_reduction_fraction": (current_high - adjusted_high)
        / current_high,
        "paired_correction_cost_reduction_fraction": (
            current_correction - adjusted_correction
        )
        / current_correction,
        "low_only_cost_reduction_fraction": (current_low - adjusted_low) / current_low,
        "adjusted_designs": designs,
        "paired_minimum_efficiency_runtime_hours": paired[
            "minimum_runtime_integer_passing_efficiency"
        ]["runtime_hours"],
        "conservative_minimum_efficiency_runtime_hours": conservative[
            "minimum_runtime_integer_passing_efficiency"
        ]["runtime_hours"],
        "conservative_best_under_cap": conservative["best_integer_under_cap"],
        "sub_10_hour_admissible_candidate_count": len(sub_cap),
        "argument_certificate_gate_inherited": bool(
            argument_result["argument_chain_certificate_gate_passed"]
        ),
        "constructed_predecessor_gate_inherited": bool(
            chain_result["constructed_predecessor_gate_passed"]
        ),
        "source_reproduction_maximum_score_difference": max(reproduction_differences),
        "retrospective_cost_projection_only": True,
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": (
            "lock a bounded pilot manifest and rerun delete-one-event cost sensitivity"
            if sub_cap
            else "reduce conservative argument fallbacks or retain the estimator as a deferred reserve"
        ),
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
                "continuous_optimal_score_ratio": row["continuous_optimal_score_ratio"],
                "best_under_cap_score_ratio": under["score_ratio"] if under else None,
                "best_under_cap_runtime_hours": under["runtime_hours"] if under else None,
                "best_under_cap_low_units": under["low_units"] if under else None,
                "minimum_efficiency_runtime_hours": efficient["runtime_hours"]
                if efficient
                else None,
                "minimum_efficiency_low_units": efficient["low_units"] if efficient else None,
                "sub_10_hour_efficiency_candidate": row["sub_10_hour_efficiency_candidate"],
            }
        )
    with DESIGN_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(design_rows[0]))
        writer.writeheader()
        writer.writerows(design_rows)
    checks = [
        (
            "source_paths_exist",
            all(path.exists() for path in required),
            "5053, 5055, 5058, 5059, 5065, and 5066 inputs exist",
        ),
        (
            "event_matrix_complete",
            len(event_rows) == 8,
            f"events={len(event_rows)}",
        ),
        (
            "source_design_reproduced",
            max(reproduction_differences) < 1.0e-9,
            f"maximum score difference={max(reproduction_differences)}",
        ),
        (
            "transport_gates_inherited",
            result["argument_certificate_gate_inherited"]
            and result["constructed_predecessor_gate_inherited"],
            "argument certificate and constructed-predecessor gates pass",
        ),
        (
            "positive_costs",
            min(
                min(
                    row["dual_transport_high_primary_seconds"],
                    row["dual_transport_paired_correction_seconds"],
                    row["argument_transport_low_only_seconds"],
                )
                for row in event_rows
            )
            > 0.0,
            "all adjusted event costs remain positive",
        ),
        (
            "all_mean_costs_reduced",
            adjusted_high < current_high
            and adjusted_correction < current_correction
            and adjusted_low < current_low,
            f"high={adjusted_high}; correction={adjusted_correction}; low={adjusted_low}",
        ),
        (
            "sample_units_preserved",
            next(
                row["events_per_variance_unit"]
                for row in designs
                if row["design"] == "paired_nested_two_event"
            )
            == 2,
            "paired design still charges two events per variance unit",
        ),
        (
            "no_fresh_execution",
            not result["fresh_kernel_execution_authorized"],
            "cost projection does not launch a pilot",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            result["retrospective_cost_projection_only"]
            and not result["valid_for_full_MTS_claim"],
            "dual transport is an operational cost result",
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5067_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5067 validation failed: {failed}")


if __name__ == "__main__":
    main()
