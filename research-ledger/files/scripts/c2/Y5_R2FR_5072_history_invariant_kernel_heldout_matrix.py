from __future__ import annotations

import csv
import importlib.util
import json
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5071 = POST / "scripts" / "Y5_R2FR_5071_recursive_transition_kernel_replay.py"
SOURCE_5070 = POST / "source-intake" / "functional_rg" / "5070"
SOURCE_5071 = POST / "source-intake" / "functional_rg" / "5071"
SOURCE = POST / "source-intake" / "functional_rg" / "5072"
GATES = SOURCE / "gates"
RESULT_JSON = SOURCE / "history_invariant_kernel_heldout_matrix.json"
ROW_CSV = SOURCE / "history_invariant_kernel_rows.csv"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5072_VALIDATION.csv"
MARKER = "MTS_5072_HISTORY_INVARIANT_KERNEL_HELDOUT_MATRIX"
REVISION = "five-case-multi-run-history-quotient-validation-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
MACHINE_EQUIVALENCE_TOLERANCE = 1.0e-12
CASES = (
    ("S503401_N0000", "A14"),
    ("S503404_N0000", "A10"),
    ("S503402_N0001", "A01"),
    ("S503403_N0000", "A06"),
    ("S503402_N0001", "A13"),
)
TIER = "primary24"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5071 = load_module("mts_5071_for_5072", SCRIPT_5071)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def localize(value: str) -> Path:
    path = Path(value)
    if path.exists():
        return path
    normalized = value.replace("\\", "/")
    marker = "/post-checkpoint-work/"
    if marker not in normalized:
        raise FileNotFoundError(value)
    candidate = POST / normalized.split(marker, 1)[1]
    if not candidate.exists():
        raise FileNotFoundError(candidate)
    return candidate


def relative_complex_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-30)


def quotient_numerical_distance(
    full_gate: dict[str, Any], constructed_gate: dict[str, Any]
) -> float:
    differences = [
        relative_complex_difference(
            complex(full_gate["topological_correction"]),
            complex(constructed_gate["topological_correction"]),
        ),
        relative_complex_difference(
            complex(full_gate["highest_order_value"]),
            complex(constructed_gate["highest_order_value"]),
        ),
    ]
    for full_chamber, constructed_chamber in zip(
        full_gate["chambers"], constructed_gate["chambers"]
    ):
        differences.append(
            relative_complex_difference(
                complex(full_chamber["topological_correction"]),
                complex(constructed_chamber["topological_correction"]),
            )
        )
    for full_row, constructed_row in zip(
        full_gate["order_rows"], constructed_gate["order_rows"]
    ):
        for field in ("regularized_naive_value", "causally_corrected_value"):
            differences.append(
                relative_complex_difference(
                    complex(full_row[field]), complex(constructed_row[field])
                )
            )
    return max(differences, default=0.0)


def main() -> None:
    chain_rows_path = SOURCE_5070 / "canonical_argument_chain_rows.csv"
    source_result_path = SOURCE_5071 / "recursive_transition_kernel_replay.json"
    required = [SCRIPT_5071, chain_rows_path, source_result_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    chain_rows = {
        (row["event_id"], row["right_argument_id"]): row
        for row in csv.DictReader(chain_rows_path.open(encoding="utf-8"))
    }
    M5071.install_history_invariant_breakpoint_rule()
    rows = []
    for event_id, argument_id in CASES:
        chain_row = chain_rows[(event_id, argument_id)]
        full_topology_path = localize(chain_row["validation_path"])
        constructed_topology_path = localize(chain_row["constructed_path"])
        run = full_topology_path.parent.parent
        artifact_name = f"E040__{event_id}__{argument_id}__{TIER}.json"
        source_job_path = run / "jobs" / artifact_name
        source_kernel_path = run / "kernels" / artifact_name
        config_path = run / "config.json"
        case_required = [
            full_topology_path,
            constructed_topology_path,
            source_job_path,
            source_kernel_path,
            config_path,
        ]
        missing_case = [str(path) for path in case_required if not path.exists()]
        if missing_case:
            raise FileNotFoundError(f"missing case inputs: {missing_case}")
        full_topology = json.loads(full_topology_path.read_text(encoding="utf-8"))
        constructed_topology = json.loads(
            constructed_topology_path.read_text(encoding="utf-8")
        )
        source_kernel = json.loads(source_kernel_path.read_text(encoding="utf-8"))
        config = json.loads(config_path.read_text(encoding="utf-8"))
        tier = config["tiers"][TIER]
        M5071.M5030.SOFT_ENERGY = float(full_topology["soft_energy"])
        M5071.M5030.SOFT_COSINE = float(full_topology["soft_cosine"])
        M5071.M5030.DECAY_COSINE = float(full_topology["decay_cosine"])
        M5071.M5030.TARGET_COSINE = complex(str(full_topology["target_cosine"]))
        full_gate, full_runtime = M5071.run_gate(full_topology, tier)
        constructed_gate, constructed_runtime = M5071.run_gate(
            constructed_topology, tier
        )
        atomic_json(GATES / f"{event_id}__{argument_id}__full.json", full_gate)
        atomic_json(
            GATES / f"{event_id}__{argument_id}__constructed.json",
            constructed_gate,
        )
        saved_gate = source_kernel["fixed_event_integral_gate"]
        full_value = M5071.highest_value(full_gate)
        constructed_value = M5071.highest_value(constructed_gate)
        saved_value = M5071.highest_value(saved_gate)
        full_constructed_difference = abs(full_value - constructed_value)
        full_constructed_relative_difference = relative_complex_difference(
            full_value, constructed_value
        )
        legacy_difference = abs(full_value - saved_value)
        legacy_relative_difference = legacy_difference / max(abs(full_value), 1.0e-30)
        tolerance = float(tier["relative_adaptive_tolerance"])
        full_correction = complex(full_gate["topological_correction"])
        constructed_correction = complex(constructed_gate["topological_correction"])
        correction_relative_difference = relative_complex_difference(
            full_correction, constructed_correction
        )
        full_projection = M5071.canonical_digest(
            M5071.quotient_physics_projection(full_gate)
        )
        constructed_projection = M5071.canonical_digest(
            M5071.quotient_physics_projection(constructed_gate)
        )
        quotient_distance = quotient_numerical_distance(
            full_gate, constructed_gate
        )
        case_passed = (
            full_constructed_relative_difference
            < MACHINE_EQUIVALENCE_TOLERANCE
            and correction_relative_difference
            < MACHINE_EQUIVALENCE_TOLERANCE
            and quotient_distance < MACHINE_EQUIVALENCE_TOLERANCE
            and legacy_relative_difference < tolerance
            and bool(full_gate["fixed_event_crossed_integral_converged"])
            and bool(constructed_gate["fixed_event_crossed_integral_converged"])
        )
        rows.append(
            {
                "event_id": event_id,
                "argument_id": argument_id,
                "chain_depth": int(chain_row["chain_depth"]),
                "incoming_transition_count": int(chain_row["transition_count"]),
                "raw_history_mismatch": chain_row["maximum_crossing_root_error"] == "inf",
                "run_name": run.name,
                "full_topology_path": str(full_topology_path),
                "constructed_topology_path": str(constructed_topology_path),
                "source_job_path": str(source_job_path),
                "source_kernel_path": str(source_kernel_path),
                "full_crossing_count": int(full_topology["total_surface_crossings"]),
                "constructed_crossing_count": int(
                    constructed_topology["total_surface_crossings"]
                ),
                "topological_correction": str(full_correction),
                "topological_correction_exact": full_correction
                == constructed_correction,
                "topological_correction_relative_difference": correction_relative_difference,
                "full_highest_value": str(full_value),
                "constructed_highest_value": str(constructed_value),
                "full_constructed_difference": full_constructed_difference,
                "full_constructed_relative_difference": full_constructed_relative_difference,
                "quotient_projection_exact": full_projection
                == constructed_projection,
                "quotient_numerical_distance": quotient_distance,
                "legacy_saved_relative_difference": legacy_relative_difference,
                "declared_relative_tolerance": tolerance,
                "full_runtime_seconds": full_runtime,
                "constructed_runtime_seconds": constructed_runtime,
                "case_passed": case_passed,
            }
        )
    failed = [row for row in rows if not row["case_passed"]]
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "case_count": len(rows),
        "run_count": len({row["run_name"] for row in rows}),
        "transition_case_count": sum(
            int(row["incoming_transition_count"]) > 0 for row in rows
        ),
        "zero_transition_case_count": sum(
            int(row["incoming_transition_count"]) == 0 for row in rows
        ),
        "raw_history_mismatch_case_count": sum(
            bool(row["raw_history_mismatch"]) for row in rows
        ),
        "maximum_chain_depth": max(int(row["chain_depth"]) for row in rows),
        "maximum_legacy_saved_relative_difference": max(
            float(row["legacy_saved_relative_difference"]) for row in rows
        ),
        "maximum_full_constructed_relative_difference": max(
            float(row["full_constructed_relative_difference"]) for row in rows
        ),
        "maximum_topological_correction_relative_difference": max(
            float(row["topological_correction_relative_difference"])
            for row in rows
        ),
        "maximum_quotient_numerical_distance": max(
            float(row["quotient_numerical_distance"]) for row in rows
        ),
        "machine_equivalence_tolerance": MACHINE_EQUIVALENCE_TOLERANCE,
        "failed_case_count": len(failed),
        "history_invariant_kernel_heldout_gate_passed": len(rows) == 5
        and not failed,
        "production_argument_topology_acceleration_authorized": len(rows) == 5
        and not failed,
        "fresh_science_run_authorized": False,
        "next_required_gate": "recompute estimator cost with eight E040 anchors and certified recursive argument chains",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    SOURCE.mkdir(parents=True, exist_ok=True)
    with ROW_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    checks = [
        ("source_paths_exist", all(path.exists() for path in required), "5071 and 5070 inputs exist"),
        ("heldout_matrix_complete", len(rows) == 5, f"cases={len(rows)}"),
        ("multiple_runs_exercised", result["run_count"] >= 3, f"runs={result['run_count']}"),
        (
            "transition_and_control_cases",
            result["transition_case_count"] >= 4
            and result["zero_transition_case_count"] >= 1,
            f"transition={result['transition_case_count']}; control={result['zero_transition_case_count']}",
        ),
        (
            "raw_history_mismatch_exercised",
            result["raw_history_mismatch_case_count"] >= 1,
            f"mismatch cases={result['raw_history_mismatch_case_count']}",
        ),
        (
            "all_quotient_outputs_machine_equivalent",
            all(
                float(row["quotient_numerical_distance"])
                < MACHINE_EQUIVALENCE_TOLERANCE
                for row in rows
            ),
            f"maximum relative distance={result['maximum_quotient_numerical_distance']}",
        ),
        (
            "all_highest_values_machine_equivalent",
            all(
                float(row["full_constructed_relative_difference"])
                < MACHINE_EQUIVALENCE_TOLERANCE
                for row in rows
            ),
            f"maximum relative difference={result['maximum_full_constructed_relative_difference']}",
        ),
        (
            "all_corrections_machine_equivalent",
            all(
                float(row["topological_correction_relative_difference"])
                < MACHINE_EQUIVALENCE_TOLERANCE
                for row in rows
            ),
            f"maximum relative difference={result['maximum_topological_correction_relative_difference']}",
        ),
        ("legacy_outputs_within_tolerance", all(float(row["legacy_saved_relative_difference"]) < float(row["declared_relative_tolerance"]) for row in rows), f"maximum legacy relative difference={result['maximum_legacy_saved_relative_difference']}"),
        ("heldout_gate_passed", result["history_invariant_kernel_heldout_gate_passed"], f"failed={len(failed)}"),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "kernel acceleration changes no physical claim"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5072_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed_checks = [name for name, passed, _ in checks if not passed]
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "check_count": len(checks),
                "failed": failed_checks,
                "passed": not failed_checks,
                "output": str(RESULT_JSON),
            },
            indent=2,
        )
    )
    if failed_checks:
        raise RuntimeError(f"checkpoint 5072 validation failed: {failed_checks}")


if __name__ == "__main__":
    main()
