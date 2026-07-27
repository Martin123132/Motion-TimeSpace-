from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5030 = POST / "scripts" / "Y5_R2FR_5030_causal_relative_collision_homotopy_gate.py"
RUN = POST / "source-intake" / "functional_rg" / "5036" / "runs" / "paired_full_vector_s2_v1"
SOURCE_5070 = POST / "source-intake" / "functional_rg" / "5070"
SOURCE = POST / "source-intake" / "functional_rg" / "5071"
EVENT_ID = "S503402_N0000"
ARGUMENT_ID = "A10"
TIER = "primary24"
FULL_TOPOLOGY = RUN / "topologies" / f"{EVENT_ID}__E040_{ARGUMENT_ID}.json"
CONSTRUCTED_TOPOLOGY = SOURCE_5070 / "constructed_argument_chains" / EVENT_ID / f"{ARGUMENT_ID}.json"
SOURCE_JOB = RUN / "jobs" / f"E040__{EVENT_ID}__{ARGUMENT_ID}__{TIER}.json"
SOURCE_KERNEL = RUN / "kernels" / f"E040__{EVENT_ID}__{ARGUMENT_ID}__{TIER}.json"
CONFIG = RUN / "config.json"
CHAIN_RESULT = SOURCE_5070 / "canonical_argument_chain_constructor_gate.json"
CHAIN_ROWS = SOURCE_5070 / "canonical_argument_chain_rows.csv"
RESULT_JSON = SOURCE / "recursive_transition_kernel_replay.json"
FULL_GATE_JSON = SOURCE / "full_topology_kernel_gate.json"
CONSTRUCTED_GATE_JSON = SOURCE / "recursive_constructed_kernel_gate.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5071_VALIDATION.csv"
MARKER = "MTS_5071_RECURSIVE_TRANSITION_KERNEL_REPLAY"
REVISION = "history-invariant-breakpoint-depth-ten-replay-v2"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5030 = load_module("mts_5030_for_5071", SCRIPT_5030)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def highest_value(gate: dict[str, Any]) -> complex:
    highest_order = max(int(value) for value in gate["relative_orders"])
    row = next(
        value
        for value in gate["order_rows"]
        if int(value["relative_order"]) == highest_order
    )
    return complex(row["causally_corrected_value"])


def physics_projection(gate: dict[str, Any]) -> dict[str, Any]:
    chambers = []
    for chamber in gate["chambers"]:
        correction_rows = sorted(
            (
                int(row["winding_correction"]),
                str(row["residue"]),
                str(row["contribution"]),
            )
            for row in chamber["correction_rows"]
        )
        chambers.append(
            {
                "residues_stable": bool(chamber["residues_stable"]),
                "topological_correction": str(chamber["topological_correction"]),
                "correction_rows": correction_rows,
            }
        )
    return {
        "relative_orders": gate["relative_orders"],
        "chambers": chambers,
        "order_rows": gate["order_rows"],
        "all_residues_stable": gate["all_residues_stable"],
        "topological_correction": gate["topological_correction"],
        "highest_order_value": gate["highest_order_value"],
        "highest_two_order_relative_residual": gate[
            "highest_two_order_relative_residual"
        ],
        "fixed_event_crossed_integral_converged": gate[
            "fixed_event_crossed_integral_converged"
        ],
    }


def quotient_physics_projection(gate: dict[str, Any]) -> dict[str, Any]:
    projection = physics_projection(gate)
    for chamber in projection["chambers"]:
        chamber.pop("correction_rows")
    return projection


def install_history_invariant_breakpoint_rule() -> None:
    original = M5030.collision_scaled_breakpoints

    def near_path_breakpoints(
        start: complex, end: complex, catalog: list[dict[str, Any]]
    ) -> list[float]:
        return original(
            start,
            end,
            [row for row in catalog if bool(row["near_path"])],
        )

    M5030.collision_scaled_breakpoints = near_path_breakpoints


def run_gate(topology: dict[str, Any], tier: dict[str, Any]) -> tuple[dict[str, Any], float]:
    started = time.perf_counter()
    gate = M5030.fixed_event_integral_gate(
        topology,
        tuple(int(value) for value in tier["relative_orders"]),
        int(tier["global_nodes"]),
        int(tier["global_residue_nodes"]),
        int(tier["relative_residue_nodes"]),
        float(tier["model_distance"]),
        64,
        str(tier["relative_quadrature_mode"]),
        float(tier["relative_adaptive_tolerance"]),
        int(tier["relative_adaptive_maximum_intervals"]),
    )
    return gate, time.perf_counter() - started


def main() -> None:
    required = [
        SCRIPT_5030,
        FULL_TOPOLOGY,
        CONSTRUCTED_TOPOLOGY,
        SOURCE_JOB,
        SOURCE_KERNEL,
        CONFIG,
        CHAIN_RESULT,
        CHAIN_ROWS,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    full_topology = json.loads(FULL_TOPOLOGY.read_text(encoding="utf-8"))
    constructed_topology = json.loads(CONSTRUCTED_TOPOLOGY.read_text(encoding="utf-8"))
    source_kernel = json.loads(SOURCE_KERNEL.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    chain_result = json.loads(CHAIN_RESULT.read_text(encoding="utf-8"))
    chain_row = next(
        row
        for row in csv.DictReader(CHAIN_ROWS.open(encoding="utf-8"))
        if row["event_id"] == EVENT_ID and row["right_argument_id"] == ARGUMENT_ID
    )
    tier = config["tiers"][TIER]
    M5030.SOFT_ENERGY = float(full_topology["soft_energy"])
    M5030.SOFT_COSINE = float(full_topology["soft_cosine"])
    M5030.DECAY_COSINE = float(full_topology["decay_cosine"])
    M5030.TARGET_COSINE = complex(str(full_topology["target_cosine"]))
    install_history_invariant_breakpoint_rule()
    full_gate, full_runtime = run_gate(full_topology, tier)
    constructed_gate, constructed_runtime = run_gate(constructed_topology, tier)
    atomic_json(FULL_GATE_JSON, full_gate)
    atomic_json(CONSTRUCTED_GATE_JSON, constructed_gate)
    saved_gate = source_kernel["fixed_event_integral_gate"]
    full_physics = canonical_digest(physics_projection(full_gate))
    constructed_physics = canonical_digest(physics_projection(constructed_gate))
    saved_physics = canonical_digest(physics_projection(saved_gate))
    full_quotient_physics = canonical_digest(quotient_physics_projection(full_gate))
    constructed_quotient_physics = canonical_digest(
        quotient_physics_projection(constructed_gate)
    )
    full_value = highest_value(full_gate)
    constructed_value = highest_value(constructed_gate)
    saved_value = highest_value(saved_gate)
    full_constructed_difference = abs(full_value - constructed_value)
    full_saved_difference = abs(full_value - saved_value)
    declared_tolerance = float(tier["relative_adaptive_tolerance"])
    full_saved_relative_difference = full_saved_difference / max(
        abs(full_value), 1.0e-30
    )
    correction = complex(full_gate["topological_correction"])
    constructed_correction = complex(constructed_gate["topological_correction"])
    correction_difference = abs(correction - constructed_correction)
    full_crossings = int(full_topology["total_surface_crossings"])
    constructed_crossings = int(constructed_topology["total_surface_crossings"])
    replay_passed = (
        constructed_quotient_physics == full_quotient_physics
        and full_constructed_difference == 0.0
        and correction_difference == 0.0
        and full_saved_relative_difference < declared_tolerance
        and abs(correction) > 0.0
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "tier": TIER,
        "chain_depth": int(chain_row["chain_depth"]),
        "incoming_transition_count": int(chain_row["transition_count"]),
        "source_was_constructed": chain_row["source_was_constructed"].lower() == "true",
        "full_topology_path": str(FULL_TOPOLOGY),
        "constructed_topology_path": str(CONSTRUCTED_TOPOLOGY),
        "source_job_path": str(SOURCE_JOB),
        "source_kernel_path": str(SOURCE_KERNEL),
        "full_surface_crossing_count": full_crossings,
        "constructed_reduced_surface_crossing_count": constructed_crossings,
        "raw_path_history_difference_count": full_crossings - constructed_crossings,
        "topological_correction": str(correction),
        "constructed_topological_correction": str(constructed_correction),
        "topological_correction_difference": correction_difference,
        "topological_correction_nonzero": abs(correction) > 0.0,
        "quadrature_breakpoint_rule": "near-path collision roots only",
        "full_gate_runtime_seconds": full_runtime,
        "constructed_gate_runtime_seconds": constructed_runtime,
        "full_physics_projection_digest": full_physics,
        "constructed_physics_projection_digest": constructed_physics,
        "saved_physics_projection_digest": saved_physics,
        "full_quotient_physics_projection_digest": full_quotient_physics,
        "constructed_quotient_physics_projection_digest": constructed_quotient_physics,
        "constructed_vs_full_physics_projection_exact": constructed_physics == full_physics,
        "constructed_vs_full_quotient_physics_projection_exact": constructed_quotient_physics
        == full_quotient_physics,
        "replayed_full_vs_saved_physics_projection_exact": full_physics == saved_physics,
        "full_highest_value": str(full_value),
        "constructed_highest_value": str(constructed_value),
        "saved_highest_value": str(saved_value),
        "constructed_vs_full_highest_value_difference": full_constructed_difference,
        "replayed_full_vs_saved_highest_value_difference": full_saved_difference,
        "replayed_full_vs_legacy_saved_relative_difference": full_saved_relative_difference,
        "declared_relative_adaptive_tolerance": declared_tolerance,
        "chain_gate_inherited": bool(chain_result["canonical_argument_chain_gate_passed"]),
        "recursive_transition_kernel_replay_passed": replay_passed,
        "history_invariant_kernel_candidate_passed": replay_passed,
        "production_argument_topology_acceleration_authorized": False,
        "fresh_science_run_authorized": False,
        "next_required_gate": "run heldout history-invariant kernel replays before estimator recosting",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", all(path.exists() for path in required), "full, recursive, job, kernel, config, and chain inputs exist"),
        ("chain_gate_inherited", result["chain_gate_inherited"], "5070 recursive argument-chain gate passed"),
        (
            "deep_transition_case",
            result["chain_depth"] == 10
            and result["incoming_transition_count"] == 22
            and result["source_was_constructed"],
            f"depth={result['chain_depth']}; transitions={result['incoming_transition_count']}",
        ),
        ("nonzero_topology_case", result["topological_correction_nonzero"], f"correction={correction}"),
        (
            "quotient_physics_projection_exact",
            result["constructed_vs_full_quotient_physics_projection_exact"],
            f"full={full_quotient_physics}; constructed={constructed_quotient_physics}",
        ),
        (
            "topological_correction_exact",
            correction_difference == 0.0,
            f"difference={correction_difference}",
        ),
        ("highest_value_exact", full_constructed_difference == 0.0, f"difference={full_constructed_difference}"),
        (
            "legacy_saved_within_declared_tolerance",
            full_saved_relative_difference < declared_tolerance,
            f"relative difference={full_saved_relative_difference}; tolerance={declared_tolerance}",
        ),
        ("recursive_kernel_replay_passed", replay_passed, "depth-ten transition-composed topology exactly reproduces the full topology under the history-invariant quadrature rule"),
        (
            "raw_history_quotient_safe",
            constructed_crossings <= full_crossings and replay_passed,
            f"full rows={full_crossings}; reduced rows={constructed_crossings}; quotient physics exact",
        ),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "kernel acceleration is operational, not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5071_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5071 validation failed: {failed_checks}")


if __name__ == "__main__":
    main()
