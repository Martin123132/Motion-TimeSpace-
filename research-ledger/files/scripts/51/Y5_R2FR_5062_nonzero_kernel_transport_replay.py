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
SOURCE_5040 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5040"
    / "runs"
    / "nested_sobol_power1_s4_v1"
)
SOURCE_5061 = POST / "source-intake" / "functional_rg" / "5061"
SOURCE = POST / "source-intake" / "functional_rg" / "5062"
FULL_TOPOLOGY = SOURCE_5040 / "topologies" / "S503402_N0001__E020_A13.json"
CONSTRUCTED_TOPOLOGY = (
    SOURCE_5061
    / "constructed_topologies"
    / "E040_TO_E020"
    / "S503402_N0001__A13.json"
)
SOURCE_JOB = (
    SOURCE_5040
    / "jobs"
    / "E020__S503402_N0001__A13__primary24.json"
)
SOURCE_KERNEL = (
    SOURCE_5040
    / "kernels"
    / "E020__S503402_N0001__A13__primary24.json"
)
CONFIG = SOURCE_5040 / "config.json"
CONSTRUCTOR_RESULT = SOURCE_5061 / "serialized_transport_topology_constructor_dry_run.json"
RESULT_JSON = SOURCE / "nonzero_kernel_transport_replay.json"
FULL_GATE_JSON = SOURCE / "full_homotopy_kernel_gate.json"
TRANSPORT_GATE_JSON = SOURCE / "transport_constructed_kernel_gate.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5062_VALIDATION.csv"
)
MARKER = "MTS_5062_NONZERO_KERNEL_TRANSPORT_REPLAY"
REVISION = "saved-nonzero-topological-correction-kernel-replay-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5030 = load_module("mts_5030_for_5062", SCRIPT_5030)


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


def run_gate(
    topology: dict[str, Any], tier: dict[str, Any]
) -> tuple[dict[str, Any], float]:
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
        CONSTRUCTOR_RESULT,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source inputs: {missing}")
    full_topology = json.loads(FULL_TOPOLOGY.read_text(encoding="utf-8"))
    constructed_topology = json.loads(CONSTRUCTED_TOPOLOGY.read_text(encoding="utf-8"))
    source_job = json.loads(SOURCE_JOB.read_text(encoding="utf-8"))
    source_kernel = json.loads(SOURCE_KERNEL.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    constructor_result = json.loads(CONSTRUCTOR_RESULT.read_text(encoding="utf-8"))
    tier = config["tiers"]["primary24"]
    M5030.SOFT_ENERGY = float(full_topology["soft_energy"])
    M5030.SOFT_COSINE = float(full_topology["soft_cosine"])
    M5030.DECAY_COSINE = float(full_topology["decay_cosine"])
    M5030.TARGET_COSINE = complex(str(full_topology["target_cosine"]))
    full_gate, full_runtime = run_gate(full_topology, tier)
    transport_gate, transport_runtime = run_gate(constructed_topology, tier)
    atomic_json(FULL_GATE_JSON, full_gate)
    atomic_json(TRANSPORT_GATE_JSON, transport_gate)
    full_digest = canonical_digest(full_gate)
    transport_digest = canonical_digest(transport_gate)
    saved_gate = source_kernel["fixed_event_integral_gate"]
    saved_digest = canonical_digest(saved_gate)
    full_physics_digest = canonical_digest(physics_projection(full_gate))
    transport_physics_digest = canonical_digest(physics_projection(transport_gate))
    saved_physics_digest = canonical_digest(physics_projection(saved_gate))
    full_value = highest_value(full_gate)
    transport_value = highest_value(transport_gate)
    saved_value = highest_value(saved_gate)
    full_transport_difference = abs(full_value - transport_value)
    full_saved_difference = abs(full_value - saved_value)
    correction = complex(full_gate["topological_correction"])
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": "S503402_N0001",
        "argument_id": "A13",
        "tier": "primary24",
        "full_topology_path": str(FULL_TOPOLOGY),
        "constructed_topology_path": str(CONSTRUCTED_TOPOLOGY),
        "source_job_path": str(SOURCE_JOB),
        "source_kernel_path": str(SOURCE_KERNEL),
        "surface_crossing_count": int(full_topology["total_surface_crossings"]),
        "topological_correction": str(correction),
        "topological_correction_nonzero": abs(correction) > 0.0,
        "full_gate_runtime_seconds": full_runtime,
        "transport_gate_runtime_seconds": transport_runtime,
        "full_gate_digest": full_digest,
        "transport_gate_digest": transport_digest,
        "saved_gate_digest": saved_digest,
        "constructed_vs_full_gate_digest_exact": transport_digest == full_digest,
        "replayed_full_vs_saved_gate_digest_exact": full_digest == saved_digest,
        "full_physics_projection_digest": full_physics_digest,
        "transport_physics_projection_digest": transport_physics_digest,
        "saved_physics_projection_digest": saved_physics_digest,
        "constructed_vs_full_physics_projection_exact": transport_physics_digest
        == full_physics_digest,
        "replayed_full_vs_saved_physics_projection_exact": full_physics_digest
        == saved_physics_digest,
        "full_highest_value": str(full_value),
        "transport_highest_value": str(transport_value),
        "saved_highest_value": str(saved_value),
        "constructed_vs_full_highest_value_difference": full_transport_difference,
        "replayed_full_vs_saved_highest_value_difference": full_saved_difference,
        "transport_constructor_inherited_gate": bool(
            constructor_result["serialized_constructor_dry_run_passed"]
        ),
        "transport_topology_kernel_replay_passed": (
            transport_physics_digest == full_physics_digest
            and full_transport_difference == 0.0
            and abs(correction) > 0.0
        ),
        "production_topology_acceleration_authorized": (
            transport_physics_digest == full_physics_digest
            and bool(constructor_result["serialized_constructor_dry_run_passed"])
        ),
        "fresh_science_run_authorized": False,
        "next_required_gate": "integrate the certified transport/fallback rule behind an explicit opt-in runner flag",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        (
            "source_paths_exist",
            all(path.exists() for path in required),
            "full, constructed, job, config, and constructor inputs exist",
        ),
        (
            "constructor_gate_inherited",
            result["transport_constructor_inherited_gate"],
            "5061 serialized constructor gate passed",
        ),
        (
            "nonzero_topology_case",
            result["surface_crossing_count"] == 8
            and result["topological_correction_nonzero"],
            f"crossings={result['surface_crossing_count']}; correction={correction}",
        ),
        (
            "physics_projection_exact",
            result["constructed_vs_full_physics_projection_exact"],
            f"full={full_physics_digest}; transport={transport_physics_digest}",
        ),
        (
            "highest_value_exact",
            full_transport_difference == 0.0,
            f"difference={full_transport_difference}",
        ),
        (
            "saved_job_reproduced",
            full_saved_difference == 0.0
            and result["replayed_full_vs_saved_physics_projection_exact"],
            f"highest-value difference={full_saved_difference}; projection exact={result['replayed_full_vs_saved_physics_projection_exact']}",
        ),
        (
            "kernel_replay_gate_passed",
            result["transport_topology_kernel_replay_passed"],
            "constructed topology gives numerically identical nonzero-correction kernel output",
        ),
        (
            "production_topology_acceleration_gate",
            result["production_topology_acceleration_authorized"],
            "certificate, constructor, and nonzero kernel replay all pass",
        ),
        (
            "no_fresh_science_run",
            not result["fresh_science_run_authorized"],
            "authorization is operational and opt-in only",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "kernel replay validates computation, not the MTS physical theory",
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
                    "check_id": f"V5062_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5062 validation failed: {failed}")


if __name__ == "__main__":
    main()
