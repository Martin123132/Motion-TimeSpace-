from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SOURCE = POST / "source-intake" / "functional_rg" / "5030"
TOPOLOGY_FILES = (
    "causal_collision_homotopy_raised_reg3e-3_steps96.json",
    "causal_collision_homotopy_direct_reg3e-3_steps96.json",
    "causal_collision_homotopy_raised_reg3e-3_steps192.json",
    "causal_collision_homotopy_raised_reg1e-3_steps96.json",
)
INTEGRAL_FILES = (
    "causal_collision_integral_global24_orders128_192.json",
    "causal_collision_integral_global32_orders128_192.json",
)


def load(name: str) -> dict[str, Any]:
    path = SOURCE / name
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def topology_signature(document: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(
        tuple(
            sorted(
                (
                    int(row["winding_correction"]),
                    round(complex(row["target_root"]).real, 9),
                    round(complex(row["target_root"]).imag, 9),
                )
                for row in chamber["surface_crossings"]
            )
        )
        for chamber in document["chambers"]
    )


def order_value(document: dict[str, Any], order: int) -> complex:
    gate = document["fixed_event_integral_gate"]
    row = next(
        row for row in gate["order_rows"] if row["relative_order"] == order
    )
    return complex(row["causally_corrected_value"])


def convergence_matrix() -> dict[str, Any]:
    topology_documents = [load(name) for name in TOPOLOGY_FILES]
    integral_documents = [load(name) for name in INTEGRAL_FILES]
    signatures = [topology_signature(document) for document in topology_documents]
    topology_invariant = all(signature == signatures[0] for signature in signatures)
    crossing_counts = [len(chamber) for chamber in signatures[0]]
    assignment_tracking_passed = all(
        document["assignment_tracking_passed"]
        for document in topology_documents
    )
    crossing_groups_consistent = all(
        document["crossing_groups_consistent"]
        for document in topology_documents
    )
    path_coverage_passed = {
        document["path_kind"] for document in topology_documents
    } == {"raised", "direct"}
    regulator_coverage_passed = {
        document["regulator"] for document in topology_documents
    } == {0.001, 0.003}
    step_coverage_passed = {
        document["homotopy_steps"] for document in topology_documents
    } == {96, 192}
    integral_gates = [
        document["fixed_event_integral_gate"]
        for document in integral_documents
    ]
    all_residues_stable = all(
        gate["all_residues_stable"] for gate in integral_gates
    )
    relative_convergence_residual = max(
        gate["highest_two_order_relative_residual"]
        for gate in integral_gates
    )
    lower_global_value = order_value(integral_documents[0], 192)
    higher_global_value = order_value(integral_documents[1], 192)
    global_absolute_difference = abs(higher_global_value - lower_global_value)
    global_relative_difference = global_absolute_difference / max(
        abs(higher_global_value), 1.0
    )
    corrections = [
        complex(gate["topological_correction"])
        for gate in integral_gates
    ]
    correction_absolute_difference = abs(corrections[1] - corrections[0])
    fixed_event_gate_passed = all(
        (
            topology_invariant,
            assignment_tracking_passed,
            crossing_groups_consistent,
            path_coverage_passed,
            regulator_coverage_passed,
            step_coverage_passed,
            all_residues_stable,
            relative_convergence_residual < 2.0e-4,
            global_relative_difference < 1.0e-3,
            correction_absolute_difference < 1.0e-8,
        )
    )
    return {
        "topology_files": list(TOPOLOGY_FILES),
        "integral_files": list(INTEGRAL_FILES),
        "topology_invariant": topology_invariant,
        "crossing_counts_by_chamber": crossing_counts,
        "assignment_tracking_passed": assignment_tracking_passed,
        "crossing_groups_consistent": crossing_groups_consistent,
        "path_coverage_passed": path_coverage_passed,
        "regulator_coverage_passed": regulator_coverage_passed,
        "step_coverage_passed": step_coverage_passed,
        "all_residues_stable": all_residues_stable,
        "maximum_relative_order_residual": relative_convergence_residual,
        "global_24_order192_value": str(lower_global_value),
        "global_32_order192_value": str(higher_global_value),
        "global_absolute_difference": global_absolute_difference,
        "global_relative_difference": global_relative_difference,
        "topological_correction_global24": str(corrections[0]),
        "topological_correction_global32": str(corrections[1]),
        "correction_absolute_difference": correction_absolute_difference,
        "reported_fixed_event_value": str(higher_global_value),
        "conservative_numeric_uncertainty": global_absolute_difference,
        "fixed_event_causal_homotopy_gate_passed": fixed_event_gate_passed,
        "full_outer_phase_space_integration_complete": False,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def csv_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    marker = "MTS_5031_CAUSAL_HOMOTOPY_FIXED_EVENT_GATE"
    return [
        {
            "gate": "topology_path_regulator_step_invariance",
            "passed": result["topology_invariant"],
            "evidence": f"crossing counts {result['crossing_counts_by_chamber']}",
            "checkpoint_marker": marker,
        },
        {
            "gate": "collision_assignment_tracking",
            "passed": result["assignment_tracking_passed"],
            "evidence": "all four topology runs pass",
            "checkpoint_marker": marker,
        },
        {
            "gate": "relative_residue_stability",
            "passed": result["all_residues_stable"],
            "evidence": "inner and outer residue circles agree or are numerical zero",
            "checkpoint_marker": marker,
        },
        {
            "gate": "relative_order_convergence",
            "passed": result["maximum_relative_order_residual"] < 2.0e-4,
            "evidence": result["maximum_relative_order_residual"],
            "checkpoint_marker": marker,
        },
        {
            "gate": "global_quadrature_convergence",
            "passed": result["global_relative_difference"] < 1.0e-3,
            "evidence": result["global_relative_difference"],
            "checkpoint_marker": marker,
        },
        {
            "gate": "fixed_event_causal_homotopy",
            "passed": result["fixed_event_causal_homotopy_gate_passed"],
            "evidence": result["reported_fixed_event_value"],
            "checkpoint_marker": marker,
        },
        {
            "gate": "full_outer_phase_space",
            "passed": False,
            "evidence": "soft energy and two polar integrations remain open",
            "checkpoint_marker": marker,
        },
        {
            "gate": "full_MTS_claim",
            "passed": False,
            "evidence": "not claimed",
            "checkpoint_marker": marker,
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-csv", type=Path)
    arguments = parser.parse_args()
    result = convergence_matrix()
    serialized = json.dumps(result, indent=2)
    if arguments.output_json is not None:
        arguments.output_json.parent.mkdir(parents=True, exist_ok=True)
        arguments.output_json.write_text(serialized + "\n", encoding="utf-8")
    if arguments.output_csv is not None:
        arguments.output_csv.parent.mkdir(parents=True, exist_ok=True)
        with arguments.output_csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=("gate", "passed", "evidence", "checkpoint_marker"),
            )
            writer.writeheader()
            writer.writerows(csv_rows(result))
    print(serialized)


if __name__ == "__main__":
    main()
