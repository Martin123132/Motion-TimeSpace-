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
SCRIPT_5055 = POST / "scripts" / "Y5_R2FR_5055_variance_cost_sample_unit_repair.py"
SOURCE_5053 = POST / "source-intake" / "functional_rg" / "5053"
SOURCE_5055 = POST / "source-intake" / "functional_rg" / "5055"
SOURCE_5057 = POST / "source-intake" / "functional_rg" / "5057"
SOURCE = POST / "source-intake" / "functional_rg" / "5058"
RESULT_JSON = SOURCE / "transport_adjusted_unit_cost_gate.json"
EVENT_CSV = SOURCE / "transport_adjusted_event_costs.csv"
DESIGN_CSV = SOURCE / "transport_adjusted_designs.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5058_VALIDATION.csv"
)
MARKER = "MTS_5058_TRANSPORT_ADJUSTED_UNIT_COST_GATE"
REVISION = "retrospective-exact-topology-transport-cost-projection-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5055 = load_module("mts_5055_for_5058", SCRIPT_5055)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def bool_value(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def main() -> None:
    source_rows_path = SOURCE_5053 / "high_low_cost_rows.csv"
    source_event_path = SOURCE_5053 / "high_low_event_costs.csv"
    source_cost_path = SOURCE_5053 / "high_low_cost_provenance_and_reuse_audit.json"
    source_design_path = SOURCE_5055 / "variance_cost_sample_unit_repair.json"
    source_transport_path = SOURCE_5057 / "direct_target_root_topology_transport_benchmark.json"
    transport_rows_path = SOURCE_5057 / "epsilon_transport_rows.csv"
    required = [
        SCRIPT_5055,
        source_rows_path,
        source_event_path,
        source_cost_path,
        source_design_path,
        source_transport_path,
        transport_rows_path,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    source_rows = list(csv.DictReader(source_rows_path.open(encoding="utf-8")))
    source_events = {
        row["event_id"]: row
        for row in csv.DictReader(source_event_path.open(encoding="utf-8"))
    }
    transport_rows = {
        (row["event_id"], row["base_argument_id"]): row
        for row in csv.DictReader(transport_rows_path.open(encoding="utf-8"))
    }
    transport_result = json.loads(source_transport_path.read_text(encoding="utf-8"))
    source_cost = json.loads(source_cost_path.read_text(encoding="utf-8"))
    source_design = json.loads(source_design_path.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in source_rows:
        grouped.setdefault(row["event_id"], []).append(row)
    event_rows = []
    for event_id, rows in sorted(grouped.items()):
        current = source_events[event_id]
        saved_topology_seconds = 0.0
        transport_seconds = 0.0
        transported_arguments = 0
        fallback_arguments = 0
        for row in rows:
            transport = transport_rows[(event_id, row["base_argument_id"])]
            if bool_value(transport["transport_attempted"]):
                saved_topology_seconds += float(row["e020_topology_runtime_seconds"])
                transport_seconds += float(transport["transport_runtime_seconds"])
                transported_arguments += 1
            else:
                fallback_arguments += 1
        net_savings = saved_topology_seconds - transport_seconds
        current_high_primary = float(current["high_primary_cost_seconds"])
        current_paired_correction = float(current["paired_high_correction_cost_seconds"])
        event_rows.append(
            {
                "event_id": event_id,
                "transported_argument_count": transported_arguments,
                "full_homotopy_fallback_argument_count": fallback_arguments,
                "saved_e020_topology_seconds": saved_topology_seconds,
                "charged_transport_seconds": transport_seconds,
                "net_topology_savings_seconds": net_savings,
                "current_high_primary_cost_seconds": current_high_primary,
                "transport_adjusted_high_primary_cost_seconds": current_high_primary
                - net_savings,
                "current_paired_correction_cost_seconds": current_paired_correction,
                "transport_adjusted_paired_correction_cost_seconds": current_paired_correction
                - net_savings,
                "low_only_cost_seconds": float(current["low_only_total_cost_seconds"]),
            }
        )
    current_high_primary = float(source_cost["mean_high_primary_event_cost_seconds"])
    current_paired_correction = float(
        source_cost["mean_paired_high_correction_event_cost_seconds"]
    )
    low_event_cost = float(source_cost["mean_low_only_total_event_cost_seconds"])
    adjusted_high_primary = float(
        np.mean([row["transport_adjusted_high_primary_cost_seconds"] for row in event_rows])
    )
    adjusted_paired_correction = float(
        np.mean(
            [row["transport_adjusted_paired_correction_cost_seconds"] for row in event_rows]
        )
    )
    mean_savings = float(np.mean([row["net_topology_savings_seconds"] for row in event_rows]))
    M5055.M5049.configure_modules()
    config = M5055.M5049.M5043.load_config()
    real_margins = np.asarray(
        [float(row["target_equivalence_margin"]) for row in config["target_precision_budgets"]]
    )
    margins = np.concatenate((real_margins, real_margins))
    adjusted_designs = []
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
            current_high_primary,
            current_paired_correction,
            low_event_cost,
        )
        adjusted = M5055.design_metrics(
            str(source_row["design"]),
            str(source_row["evidence_role"]),
            int(source_row["events_per_variance_unit"]),
            variance_high,
            variance_correction,
            variance_low,
            margins,
            adjusted_high_primary,
            adjusted_paired_correction,
            low_event_cost,
        )
        reproduction_differences.append(
            abs(
                float(reproduced["continuous_optimal_score_ratio"])
                - float(source_row["continuous_optimal_score_ratio"])
            )
        )
        adjusted_designs.append(adjusted)
    admissible = [
        row
        for row in adjusted_designs
        if row["evidence_role"]
        in {"admissible paired design", "admissible conservative envelope"}
    ]
    sub_cap = [row for row in admissible if row["sub_10_hour_efficiency_candidate"]]
    conservative = next(
        row for row in adjusted_designs if row["design"] == "single_componentwise_conservative"
    )
    paired = next(
        row for row in adjusted_designs if row["design"] == "paired_nested_two_event"
    )
    formal_digest = M5055.M5049.M5043.tree_digest(POST.parent / "formalization-workbench")
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "transport_benchmark_passed": bool(
            transport_result["hybrid_e040_to_e020_transport_authorized_for_benchmark"]
        ),
        "event_count": len(event_rows),
        "transported_argument_count": sum(
            int(row["transported_argument_count"]) for row in event_rows
        ),
        "full_homotopy_fallback_argument_count": sum(
            int(row["full_homotopy_fallback_argument_count"]) for row in event_rows
        ),
        "mean_net_topology_savings_seconds": mean_savings,
        "mean_current_high_primary_event_cost_seconds": current_high_primary,
        "mean_transport_adjusted_high_primary_event_cost_seconds": adjusted_high_primary,
        "mean_current_paired_correction_event_cost_seconds": current_paired_correction,
        "mean_transport_adjusted_paired_correction_event_cost_seconds": adjusted_paired_correction,
        "mean_low_only_event_cost_seconds": low_event_cost,
        "high_primary_cost_reduction_fraction": mean_savings / current_high_primary,
        "paired_correction_cost_reduction_fraction": mean_savings
        / current_paired_correction,
        "adjusted_designs": adjusted_designs,
        "paired_minimum_efficiency_runtime_hours": paired[
            "minimum_runtime_integer_passing_efficiency"
        ]["runtime_hours"],
        "conservative_minimum_efficiency_runtime_hours": conservative[
            "minimum_runtime_integer_passing_efficiency"
        ]["runtime_hours"],
        "conservative_best_under_cap": conservative["best_integer_under_cap"],
        "sub_10_hour_admissible_candidate_count": len(sub_cap),
        "retrospective_cost_projection_only": True,
        "production_shortcut_authorized": False,
        "production_blocker": (
            "an a-priori structural-transition certificate is required so fallback can be selected without computing the full E020 homotopy"
        ),
        "fresh_kernel_execution_authorized": False,
        "next_required_gate": "build a short epsilon-segment structural-transition certificate",
        "source_reproduction_maximum_score_difference": max(reproduction_differences),
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    SOURCE.mkdir(parents=True, exist_ok=True)
    with EVENT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(event_rows[0]))
        writer.writeheader()
        writer.writerows(event_rows)
    design_rows = []
    for row in adjusted_designs:
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
            "5053, 5055, and 5057 inputs exist",
        ),
        (
            "source_design_reproduced",
            max(reproduction_differences) < 1.0e-9,
            f"maximum score difference={max(reproduction_differences)}",
        ),
        (
            "transport_scope_complete",
            result["transported_argument_count"] == 119
            and result["full_homotopy_fallback_argument_count"] == 1,
            "119 transported arguments and one charged full-homotopy fallback",
        ),
        (
            "positive_measured_savings",
            mean_savings > 0.0
            and adjusted_high_primary < current_high_primary
            and adjusted_paired_correction < current_paired_correction,
            f"mean net savings={mean_savings} seconds",
        ),
        (
            "cost_identity",
            abs((current_high_primary - mean_savings) - adjusted_high_primary) < 1.0e-8
            and abs((current_paired_correction - mean_savings) - adjusted_paired_correction)
            < 1.0e-8,
            "adjusted event costs subtract only validated net topology savings",
        ),
        (
            "sample_units_preserved",
            next(
                row["events_per_variance_unit"]
                for row in adjusted_designs
                if row["design"] == "paired_nested_two_event"
            )
            == 2,
            "paired variance unit remains two events",
        ),
        (
            "production_gate_closed",
            not result["production_shortcut_authorized"]
            and bool(result["production_blocker"]),
            "retrospective exactness does not replace an a-priori fallback certificate",
        ),
        (
            "no_fresh_execution",
            not result["fresh_kernel_execution_authorized"],
            "no fresh kernel run authorized by a cost projection",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "claim_discipline",
            result["retrospective_cost_projection_only"]
            and not result["valid_for_full_MTS_claim"],
            "cost result is operational rather than physical evidence",
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
                    "check_id": f"V5058_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5058 validation failed: {failed}")


if __name__ == "__main__":
    main()
