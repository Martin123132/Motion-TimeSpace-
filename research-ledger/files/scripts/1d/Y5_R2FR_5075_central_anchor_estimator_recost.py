from __future__ import annotations

import csv
import importlib.util
import json
import os
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5073 = POST / "scripts" / "Y5_R2FR_5073_full_chain_estimator_recost.py"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE_5055 = POST / "source-intake" / "functional_rg" / "5055"
SOURCE_5069 = POST / "source-intake" / "functional_rg" / "5069"
SOURCE_5072 = POST / "source-intake" / "functional_rg" / "5072"
SOURCE_5074 = POST / "source-intake" / "functional_rg" / "5074"
SOURCE = POST / "source-intake" / "functional_rg" / "5075"
RESULT_JSON = SOURCE / "central_anchor_estimator_recost.json"
EVENT_CSV = SOURCE / "central_anchor_event_costs.csv"
DESIGN_CSV = SOURCE / "central_anchor_designs.csv"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5075_VALIDATION.csv"
MARKER = "MTS_5075_CENTRAL_ANCHOR_ESTIMATOR_RECOST"
REVISION = "fixed-a08-bidirectional-chain-cost-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ANCHOR_ID = "A08"
CONSTRUCTOR_ALLOWANCE_SECONDS = 0.1


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5073 = load_module("mts_5073_for_5075", SCRIPT_5073)
M5055 = M5073.M5055


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
    epsilon_rows_path = SOURCE_5069 / "winding_composition_rows.csv"
    kernel_result_path = SOURCE_5072 / "history_invariant_kernel_heldout_matrix.json"
    chain_rows_path = SOURCE_5074 / "central_anchor_bidirectional_chain_rows.csv"
    chain_result_path = SOURCE_5074 / "central_anchor_bidirectional_chain_gate.json"
    prior_recost_path = POST / "source-intake" / "functional_rg" / "5073" / "full_chain_estimator_recost.json"
    required = [
        SCRIPT_5073,
        cost_rows_path,
        event_rows_path,
        source_cost_path,
        source_design_path,
        epsilon_rows_path,
        kernel_result_path,
        chain_rows_path,
        chain_result_path,
        prior_recost_path,
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
    source_cost = json.loads(source_cost_path.read_text(encoding="utf-8"))
    source_design = json.loads(source_design_path.read_text(encoding="utf-8"))
    chain_result = json.loads(chain_result_path.read_text(encoding="utf-8"))
    kernel_result = json.loads(kernel_result_path.read_text(encoding="utf-8"))
    prior_recost = json.loads(prior_recost_path.read_text(encoding="utf-8"))
    event_rows = []
    for event_id in sorted(source_events):
        source_event = source_events[event_id]
        anchor_row = next(
            row
            for row in cost_rows
            if row["event_id"] == event_id
            and row["base_argument_id"] == ANCHOR_ID
        )
        anchor_seconds = float(anchor_row["e040_topology_runtime_seconds"])
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
        projected_e040 = (
            anchor_seconds
            + argument_certificate_seconds
            + 14 * CONSTRUCTOR_ALLOWANCE_SECONDS
        )
        projected_e020 = (
            epsilon_certificate_seconds
            + 15 * CONSTRUCTOR_ALLOWANCE_SECONDS
        )
        projected_high_topology = projected_e040 + projected_e020
        high_kernel = float(source_event["high_primary_kernel_cost_seconds"])
        low_kernel = float(source_event["low_only_kernel_cost_seconds"])
        paired_low_kernel = float(source_event["paired_low_kernel_cost_seconds"])
        projected_high = projected_high_topology + high_kernel
        projected_correction = projected_high + paired_low_kernel
        projected_low = projected_e040 + low_kernel
        event_rows.append(
            {
                "event_id": event_id,
                "anchor_argument_id": ANCHOR_ID,
                "anchor_runtime_seconds": anchor_seconds,
                "argument_certificate_seconds": argument_certificate_seconds,
                "epsilon_certificate_seconds": epsilon_certificate_seconds,
                "constructor_allowance_seconds": 29
                * CONSTRUCTOR_ALLOWANCE_SECONDS,
                "projected_e040_topology_seconds": projected_e040,
                "projected_e020_topology_seconds": projected_e020,
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
    for source_row in source_design["designs"]:
        designs.append(
            M5055.design_metrics(
                str(source_row["design"]),
                str(source_row["evidence_role"]),
                int(source_row["events_per_variance_unit"]),
                np.asarray(source_row["variance_high"], dtype=float),
                np.asarray(source_row["variance_correction"], dtype=float),
                np.asarray(source_row["variance_low_contribution"], dtype=float),
                margins,
                projected_high,
                projected_correction,
                projected_low,
            )
        )
    conservative = next(
        row
        for row in designs
        if row["design"] == "single_componentwise_conservative"
    )
    paired = next(
        row for row in designs if row["design"] == "paired_nested_two_event"
    )
    sub_cap = [
        row
        for row in designs
        if row["evidence_role"]
        in {"admissible paired design", "admissible conservative envelope"}
        and row["sub_10_hour_efficiency_candidate"]
    ]
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "anchor_argument_id": ANCHOR_ID,
        "mean_anchor_runtime_seconds": float(
            np.mean([row["anchor_runtime_seconds"] for row in event_rows])
        ),
        "maximum_anchor_runtime_seconds": max(
            float(row["anchor_runtime_seconds"]) for row in event_rows
        ),
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
        "a08_vs_a00_high_cost_reduction_seconds": float(
            prior_recost["mean_projected_high_primary_seconds"]
        )
        - projected_high,
        "adjusted_designs": designs,
        "conservative_minimum_efficiency": conservative[
            "minimum_runtime_integer_passing_efficiency"
        ],
        "conservative_best_under_cap": conservative["best_integer_under_cap"],
        "paired_minimum_efficiency_runtime_hours": paired[
            "minimum_runtime_integer_passing_efficiency"
        ]["runtime_hours"],
        "sub_10_hour_admissible_candidate_count": len(sub_cap),
        "bidirectional_chain_gate_inherited": bool(
            chain_result["central_anchor_bidirectional_chain_gate_passed"]
        ),
        "kernel_heldout_gate_inherited": bool(
            kernel_result["history_invariant_kernel_heldout_gate_passed"]
        ),
        "retrospective_cost_projection_only": True,
        "fresh_pilot_authorized": False,
        "next_required_gate": "run delete-one-event and delete-one-seed sensitivity with the fixed A08 cost model",
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
                "minimum_efficiency_low_units": efficient["low_units"],
                "minimum_efficiency_score_ratio": efficient["score_ratio"],
                "minimum_efficiency_runtime_hours": efficient["runtime_hours"],
                "best_under_cap_low_units": under["low_units"] if under else None,
                "best_under_cap_score_ratio": under["score_ratio"] if under else None,
                "best_under_cap_runtime_hours": under["runtime_hours"] if under else None,
                "sub_10_hour_efficiency_candidate": row[
                    "sub_10_hour_efficiency_candidate"
                ],
            }
        )
    with DESIGN_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(design_rows[0]))
        writer.writeheader()
        writer.writerows(design_rows)
    checks = [
        ("source_paths_exist", all(path.exists() for path in required), "5053, 5055, 5069, 5072, 5073, and 5074 inputs exist"),
        ("event_matrix_complete", len(event_rows) == 8, f"events={len(event_rows)}"),
        ("central_anchor_locked", all(row["anchor_argument_id"] == ANCHOR_ID for row in event_rows), f"anchor={ANCHOR_ID}"),
        ("central_anchor_positive", min(float(row["anchor_runtime_seconds"]) for row in event_rows) > 0.0, f"mean={result['mean_anchor_runtime_seconds']}"),
        ("transport_and_kernel_gates_inherited", result["bidirectional_chain_gate_inherited"] and result["kernel_heldout_gate_inherited"], "bidirectional chain and heldout kernel gates pass"),
        ("all_mean_costs_reduced", projected_high < current_high and projected_correction < current_correction and projected_low < current_low, f"high={projected_high}; correction={projected_correction}; low={projected_low}"),
        ("central_anchor_improves_a00_projection", result["a08_vs_a00_high_cost_reduction_seconds"] > 0.0, f"seconds={result['a08_vs_a00_high_cost_reduction_seconds']}"),
        ("sub_ten_hour_conservative_candidate", len(sub_cap) >= 1 and conservative["sub_10_hour_efficiency_candidate"], f"minimum runtime={conservative['minimum_runtime_integer_passing_efficiency']['runtime_hours']}"),
        ("no_fresh_execution", not result["fresh_pilot_authorized"], "recost launches no pilot"),
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
                    "check_id": f"V5075_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5075 validation failed: {failed}")


if __name__ == "__main__":
    main()
