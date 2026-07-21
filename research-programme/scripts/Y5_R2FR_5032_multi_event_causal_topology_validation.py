from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SOURCE = POST / "source-intake" / "functional_rg" / "5032"
GRID_FILE = SOURCE / "multi_event_causal_topology_grid.json"
INTEGRAL_FILES = (
    SOURCE / "corrected_baseline_integral_global24_orders128_192.json",
    SOURCE / "corrected_baseline_integral_global32_orders128_192.json",
)
OLD_MATRIX = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5031"
    / "causal_homotopy_convergence_matrix.json"
)
MARKER = "MTS_5032_PROJECTIVE_CAUSAL_TOPOLOGY_GRID_GATE"


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def highest_value(document: dict[str, Any]) -> complex:
    gate = document["fixed_event_integral_gate"]
    highest_order = max(gate["relative_orders"])
    row = next(
        row
        for row in gate["order_rows"]
        if row["relative_order"] == highest_order
    )
    return complex(row["causally_corrected_value"])


def validation() -> dict[str, Any]:
    grid = load(GRID_FILE)
    integrals = [load(path) for path in INTEGRAL_FILES]
    old_matrix = load(OLD_MATRIX)
    required_rows = [
        row for row in grid["refinement_rows"] if row["required_for_gate"]
    ]
    regulator_rows = [
        row for row in required_rows if row["variant"] == "smaller_regulator"
    ]
    step_rows = [
        row for row in required_rows if row["variant"] == "double_steps"
    ]
    maximum_grid_projective_step = max(
        row["maximum_assignment_projective_step"] for row in grid["grid_rows"]
    )
    maximum_refinement_projective_step = max(
        row["maximum_assignment_projective_step"] for row in required_rows
    )
    topology_gate_passed = all(
        (
            grid["grid_event_count"] == 9,
            grid["topology_class_count"] == 8,
            grid["required_failure_count"] == 0,
            grid["grid_topology_gate_passed"],
            grid["class_refinement_gate_passed"],
            grid["multi_event_causal_topology_gate_passed"],
            all(row["topology_scan_passed"] for row in grid["grid_rows"]),
            maximum_grid_projective_step < 0.1,
            maximum_refinement_projective_step < 0.1,
        )
    )
    regulator_limit_passed = len(regulator_rows) == 8 and all(
        row["refinement_passed"] for row in regulator_rows
    )
    step_refinement_passed = len(step_rows) == 8 and all(
        row["refinement_passed"] for row in step_rows
    )
    path_prescription_nontrivial = (
        0 < grid["path_diagnostic_match_count"] < grid["path_diagnostic_total"]
    )
    crossing_counts = [
        chamber["surface_crossing_count"]
        for chamber in integrals[1]["chambers"]
    ]
    integral_gates = [
        document["fixed_event_integral_gate"] for document in integrals
    ]
    all_residues_stable = all(
        gate["all_residues_stable"] for gate in integral_gates
    )
    correction_rows = [
        row
        for gate in integral_gates
        for chamber in gate["chambers"]
        for row in chamber["correction_rows"]
    ]
    all_crossed_residues_numerically_zero = bool(correction_rows) and all(
        complex(row["residue"]) == 0.0j for row in correction_rows
    )
    relative_order_residual = max(
        gate["highest_two_order_relative_residual"] for gate in integral_gates
    )
    values = [highest_value(document) for document in integrals]
    global_absolute_difference = abs(values[1] - values[0])
    global_relative_difference = global_absolute_difference / max(
        abs(values[1]), 1.0
    )
    corrections = [
        complex(gate["topological_correction"]) for gate in integral_gates
    ]
    correction_absolute_difference = abs(corrections[1] - corrections[0])
    corrected_integral_gate_passed = all(
        (
            crossing_counts == [0, 2, 0, 2],
            all_residues_stable,
            all_crossed_residues_numerically_zero,
            relative_order_residual < 2.0e-4,
            global_relative_difference < 1.0e-3,
            correction_absolute_difference < 1.0e-8,
            all(
                gate["fixed_event_crossed_integral_converged"]
                for gate in integral_gates
            ),
        )
    )
    old_value = complex(old_matrix["reported_fixed_event_value"])
    supersedes_5031 = (
        old_matrix["crossing_counts_by_chamber"] != crossing_counts
        and abs(values[1] - old_value) > global_absolute_difference
    )
    claim_boundary_passed = all(
        (
            not grid["outer_phase_space_integration_complete"],
            not grid["full_coupled_cut_bridge_complete"],
            not grid["valid_for_full_MTS_claim"],
            all(
                not document["full_coupled_cut_bridge_complete"]
                and not document["valid_for_full_MTS_claim"]
                for document in integrals
            ),
        )
    )
    checkpoint_gate_passed = all(
        (
            topology_gate_passed,
            regulator_limit_passed,
            step_refinement_passed,
            path_prescription_nontrivial,
            corrected_integral_gate_passed,
            supersedes_5031,
            claim_boundary_passed,
        )
    )
    return {
        "checkpoint_marker": MARKER,
        "grid_file": str(GRID_FILE),
        "integral_files": [str(path) for path in INTEGRAL_FILES],
        "superseded_matrix": str(OLD_MATRIX),
        "grid_event_count": grid["grid_event_count"],
        "topology_class_count": grid["topology_class_count"],
        "representative_event_ids": grid["representative_event_ids"],
        "maximum_grid_projective_step": maximum_grid_projective_step,
        "maximum_required_refinement_projective_step": (
            maximum_refinement_projective_step
        ),
        "topology_gate_passed": topology_gate_passed,
        "regulator_limit_refinement_passed": regulator_limit_passed,
        "step_refinement_passed": step_refinement_passed,
        "path_diagnostic_match_count": grid["path_diagnostic_match_count"],
        "path_diagnostic_total": grid["path_diagnostic_total"],
        "canonical_path_prescription_nontrivial": path_prescription_nontrivial,
        "corrected_crossing_counts_by_chamber": crossing_counts,
        "all_residues_stable": all_residues_stable,
        "all_crossed_residues_numerically_zero": (
            all_crossed_residues_numerically_zero
        ),
        "maximum_relative_order_residual": relative_order_residual,
        "global_24_order192_value": str(values[0]),
        "global_32_order192_value": str(values[1]),
        "global_absolute_difference": global_absolute_difference,
        "global_relative_difference": global_relative_difference,
        "topological_correction_global24": str(corrections[0]),
        "topological_correction_global32": str(corrections[1]),
        "correction_absolute_difference": correction_absolute_difference,
        "corrected_fixed_event_integral_gate_passed": (
            corrected_integral_gate_passed
        ),
        "superseded_5031_crossing_counts": old_matrix[
            "crossing_counts_by_chamber"
        ],
        "superseded_5031_reported_value": str(old_value),
        "absolute_change_from_5031": abs(values[1] - old_value),
        "checkpoint_5031_superseded": supersedes_5031,
        "reported_corrected_fixed_event_value": str(values[1]),
        "conservative_numeric_uncertainty": global_absolute_difference,
        "claim_boundary_passed": claim_boundary_passed,
        "checkpoint_gate_passed": checkpoint_gate_passed,
        "outer_phase_space_integration_complete": False,
        "full_coupled_cut_bridge_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def csv_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "nine_event_projective_topology_grid",
            "passed": result["topology_gate_passed"],
            "evidence": (
                f"{result['grid_event_count']} events, "
                f"{result['topology_class_count']} classes"
            ),
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "regulator_limit_refinement",
            "passed": result["regulator_limit_refinement_passed"],
            "evidence": "all eight representatives stable under epsilon/10",
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "homotopy_step_refinement",
            "passed": result["step_refinement_passed"],
            "evidence": "all eight representatives stable under step doubling",
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "canonical_path_prescription",
            "passed": result["canonical_path_prescription_nontrivial"],
            "evidence": (
                f"{result['path_diagnostic_match_count']}/"
                f"{result['path_diagnostic_total']} alternatives match"
            ),
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "corrected_fixed_event_integral",
            "passed": result["corrected_fixed_event_integral_gate_passed"],
            "evidence": result["reported_corrected_fixed_event_value"],
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "5031_supersession_recorded",
            "passed": result["checkpoint_5031_superseded"],
            "evidence": (
                f"crossings {result['superseded_5031_crossing_counts']} -> "
                f"{result['corrected_crossing_counts_by_chamber']}"
            ),
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "outer_phase_space",
            "passed": False,
            "evidence": "x and two polar integrations remain open",
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "full_MTS_claim",
            "passed": False,
            "evidence": "not claimed",
            "checkpoint_marker": MARKER,
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-csv", type=Path)
    arguments = parser.parse_args()
    result = validation()
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
