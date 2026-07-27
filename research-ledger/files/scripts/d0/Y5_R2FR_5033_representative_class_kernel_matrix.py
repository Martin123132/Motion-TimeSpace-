from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5032 = POST / "scripts" / "Y5_R2FR_5032_multi_event_causal_topology_grid.py"
SOURCE_5032 = POST / "source-intake" / "functional_rg" / "5032"
SOURCE = POST / "source-intake" / "functional_rg" / "5033"
GRID_FILE = SOURCE_5032 / "multi_event_causal_topology_grid.json"
TIERS = {
    "global24": {
        "relative_orders": (24,),
        "global_nodes": 24,
        "global_residue_nodes": 24,
        "relative_residue_nodes": 20,
        "model_distance": 0.65,
        "relative_quadrature_mode": "collision_scaled_adaptive",
        "relative_quadrature_revision": "collision-scaled-adaptive-v1",
        "relative_adaptive_tolerance": 5.0e-5,
        "relative_adaptive_maximum_intervals": 1024,
        "global_cycle_revision": "conditioned-subminimum-annulus-v5",
        "relative_residue_revision": "pair-local-double-residue-adaptive-v3",
    },
    "global32": {
        "relative_orders": (24,),
        "global_nodes": 32,
        "global_residue_nodes": 32,
        "relative_residue_nodes": 24,
        "model_distance": 0.65,
        "relative_quadrature_mode": "collision_scaled_adaptive",
        "relative_quadrature_revision": "collision-scaled-adaptive-v1",
        "relative_adaptive_tolerance": 5.0e-5,
        "relative_adaptive_maximum_intervals": 1024,
        "global_cycle_revision": "conditioned-subminimum-annulus-v5",
        "relative_residue_revision": "pair-local-double-residue-adaptive-v3",
    },
}
MARKER = "MTS_5033_REPRESENTATIVE_CLASS_KERNEL_MATRIX_GATE"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5032 = load_module("mts_5032_for_5033", SCRIPT_5032)
M5030 = M5032.M5030


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def gate_matches_tier(document: dict[str, Any], tier: dict[str, Any]) -> bool:
    gate = document.get("fixed_event_integral_gate", {})
    return (
        tuple(gate.get("relative_orders", ())) == tier["relative_orders"]
        and gate.get("global_nodes") == tier["global_nodes"]
        and gate.get("global_residue_nodes") == tier["global_residue_nodes"]
        and gate.get("relative_residue_nodes") == tier["relative_residue_nodes"]
        and gate.get("model_distance") == tier["model_distance"]
        and gate.get("relative_quadrature_mode")
        == tier["relative_quadrature_mode"]
        and gate.get("relative_quadrature_revision")
        == tier["relative_quadrature_revision"]
        and gate.get("relative_adaptive_tolerance")
        == tier["relative_adaptive_tolerance"]
        and gate.get("relative_adaptive_maximum_intervals")
        == tier["relative_adaptive_maximum_intervals"]
        and gate.get("global_cycle_revision") == tier["global_cycle_revision"]
        and gate.get("relative_residue_revision")
        == tier["relative_residue_revision"]
    )


def run_kernel(
    class_id: str,
    event: dict[str, Any],
    topology_file: Path,
    tier_name: str,
    reuse_existing: bool,
) -> tuple[dict[str, Any], Path]:
    tier = TIERS[tier_name]
    output = (
        SOURCE
        / "kernels"
        / f"{class_id}_{event['event_id']}_{tier_name}_adaptive_order24.json"
    )
    if reuse_existing and output.exists():
        candidate = load_json(output)
        if (
            candidate.get("event_id") == event["event_id"]
            and candidate.get("topology_class_id") == class_id
            and candidate.get("topology_source_file") == str(topology_file)
            and candidate.get("quadrature_tier") == tier_name
            and gate_matches_tier(candidate, tier)
        ):
            return candidate, output
    topology = load_json(topology_file)
    if not (
        topology.get("event_id") == event["event_id"]
        and topology["assignment_tracking_passed"]
        and topology["crossing_groups_consistent"]
    ):
        raise RuntimeError(f"unvalidated topology source for {event['event_id']}")
    M5032.configure_event(event)
    integral = M5030.fixed_event_integral_gate(
        topology,
        tier["relative_orders"],
        tier["global_nodes"],
        tier["global_residue_nodes"],
        tier["relative_residue_nodes"],
        tier["model_distance"],
        64,
        tier["relative_quadrature_mode"],
        tier["relative_adaptive_tolerance"],
        tier["relative_adaptive_maximum_intervals"],
    )
    document = dict(topology)
    document.update(
        {
            "event_id": event["event_id"],
            "topology_class_id": class_id,
            "topology_source_file": str(topology_file),
            "quadrature_tier": tier_name,
            "fixed_event_integral_gate": integral,
            "relative_residue_corrections_evaluated": True,
            "fixed_event_crossed_integral_converged": integral[
                "fixed_event_crossed_integral_converged"
            ],
            "outer_phase_space_integration_complete": False,
            "full_coupled_cut_bridge_complete": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return document, output


def highest_value(document: dict[str, Any]) -> complex:
    gate = document["fixed_event_integral_gate"]
    highest_order = max(gate["relative_orders"])
    row = next(
        row
        for row in gate["order_rows"]
        if row["relative_order"] == highest_order
    )
    return complex(row["causally_corrected_value"])


def correction_statistics(document: dict[str, Any]) -> tuple[int, int]:
    rows = [
        row
        for chamber in document["fixed_event_integral_gate"]["chambers"]
        for row in chamber["correction_rows"]
    ]
    nonzero = sum(complex(row["residue"]) != 0.0j for row in rows)
    return len(rows), nonzero


def class_summary(
    class_id: str,
    event_id: str,
    topology: dict[str, Any],
    documents: dict[str, dict[str, Any]],
    output_files: dict[str, Path],
) -> dict[str, Any]:
    low = documents["global24"]
    high = documents["global32"]
    gates = [low["fixed_event_integral_gate"], high["fixed_event_integral_gate"]]
    values = [highest_value(low), highest_value(high)]
    corrections = [complex(gate["topological_correction"]) for gate in gates]
    global_absolute_difference = abs(values[1] - values[0])
    global_relative_difference = global_absolute_difference / max(
        abs(values[1]), 1.0
    )
    correction_absolute_difference = abs(corrections[1] - corrections[0])
    correction_relative_scale = correction_absolute_difference / max(
        abs(corrections[1]), 1.0
    )
    maximum_relative_order_residual = max(
        gate["highest_two_order_relative_residual"] for gate in gates
    )
    all_residues_stable = all(gate["all_residues_stable"] for gate in gates)
    crossed_count, nonzero_count = correction_statistics(high)
    class_kernel_gate_passed = all(
        (
            topology["assignment_tracking_passed"],
            topology["crossing_groups_consistent"],
            all_residues_stable,
            all(gate["fixed_event_crossed_integral_converged"] for gate in gates),
            maximum_relative_order_residual < 2.0e-4,
            global_relative_difference < 1.0e-3,
            correction_relative_scale < 1.0e-6,
        )
    )
    return {
        "class_id": class_id,
        "representative_event_id": event_id,
        "crossing_counts": [
            chamber["surface_crossing_count"] for chamber in topology["chambers"]
        ],
        "global24_output": str(output_files["global24"]),
        "global32_output": str(output_files["global32"]),
        "global24_highest_order_value": str(values[0]),
        "global32_highest_order_value": str(values[1]),
        "global_absolute_difference": global_absolute_difference,
        "global_relative_difference": global_relative_difference,
        "topological_correction_global24": str(corrections[0]),
        "topological_correction_global32": str(corrections[1]),
        "correction_absolute_difference": correction_absolute_difference,
        "correction_relative_scale": correction_relative_scale,
        "crossed_residue_count": crossed_count,
        "nonzero_crossed_residue_count": nonzero_count,
        "all_residues_stable": all_residues_stable,
        "maximum_relative_order_residual": maximum_relative_order_residual,
        "class_kernel_gate_passed": class_kernel_gate_passed,
    }


def matrix(reuse_existing: bool) -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    grid = load_json(GRID_FILE)
    event_rows = {row["event_id"]: row for row in grid["grid_rows"]}
    class_rows = sorted(grid["topology_classes"], key=lambda row: row["class_id"])
    summaries: list[dict[str, Any]] = []
    for class_row in class_rows:
        class_id = class_row["class_id"]
        event_id = class_row["representative_event_id"]
        event = event_rows[event_id]
        topology_file = SOURCE_5032 / "events" / event["output_file"]
        topology = load_json(topology_file)
        documents: dict[str, dict[str, Any]] = {}
        output_files: dict[str, Path] = {}
        for tier_name, tier in TIERS.items():
            print(f"running {class_id} {event_id} {tier_name}", flush=True)
            document, output = run_kernel(
                class_id,
                event,
                topology_file,
                tier_name,
                reuse_existing,
            )
            documents[tier_name] = document
            output_files[tier_name] = output
        summary = class_summary(
            class_id, event_id, topology, documents, output_files
        )
        summaries.append(summary)
        print(
            f"completed {class_id}: pass={summary['class_kernel_gate_passed']} "
            f"global={summary['global_relative_difference']:.3e} "
            f"relative={summary['maximum_relative_order_residual']:.3e}",
            flush=True,
        )
    failed_classes = [
        row["class_id"] for row in summaries if not row["class_kernel_gate_passed"]
    ]
    gate_passed = len(summaries) == 8 and not failed_classes
    return {
        "checkpoint_marker": MARKER,
        "grid_file": str(GRID_FILE),
        "quadrature_tiers": TIERS,
        "class_rows": summaries,
        "representative_class_count": len(summaries),
        "failed_class_ids": failed_classes,
        "all_representative_class_kernels_passed": gate_passed,
        "representative_class_kernel_matrix_complete": gate_passed,
        "outer_phase_space_integration_complete": False,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def csv_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "gate": f"{row['class_id']}_{row['representative_event_id']}",
            "passed": row["class_kernel_gate_passed"],
            "evidence": (
                f"global={row['global_relative_difference']};"
                f"relative={row['maximum_relative_order_residual']};"
                f"value={row['global32_highest_order_value']}"
            ),
            "checkpoint_marker": MARKER,
        }
        for row in result["class_rows"]
    ]
    rows.extend(
        (
            {
                "gate": "outer_phase_space",
                "passed": False,
                "evidence": "not run before representative-class completion",
                "checkpoint_marker": MARKER,
            },
            {
                "gate": "full_MTS_claim",
                "passed": False,
                "evidence": "not claimed",
                "checkpoint_marker": MARKER,
            },
        )
    )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-json",
        type=Path,
        default=SOURCE / "representative_class_kernel_matrix.json",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=SOURCE / "representative_class_kernel_gate.csv",
    )
    parser.add_argument("--no-reuse-existing", action="store_true")
    arguments = parser.parse_args()
    result = matrix(not arguments.no_reuse_existing)
    arguments.output_json.parent.mkdir(parents=True, exist_ok=True)
    arguments.output_json.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    with arguments.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("gate", "passed", "evidence", "checkpoint_marker"),
        )
        writer.writeheader()
        writer.writerows(csv_rows(result))
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "representative_class_count": result[
                    "representative_class_count"
                ],
                "failed_class_ids": result["failed_class_ids"],
                "gate_passed": result[
                    "all_representative_class_kernels_passed"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
