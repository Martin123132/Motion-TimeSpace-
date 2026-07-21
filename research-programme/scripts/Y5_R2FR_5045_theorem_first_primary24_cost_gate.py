from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5043 = POST / "scripts" / "Y5_R2FR_5043_theorem_first_coarse_E040_multilevel_gate.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5045"
RUN = SOURCE / "runs" / "theorem_first_primary24_v1"
BENCHMARK_JSON = SOURCE / "primary24_benchmark.json"
RESULT_JSON = SOURCE / "primary24_full_event_cost_gate.json"
COST_CSV = SOURCE / "cost_repricing.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5045_VALIDATION.csv"
)
MARKER = "MTS_5045_THEOREM_FIRST_PRIMARY24_COST_GATE"
REVISION = "primary24-theorem-first-cross-source-zero-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S503401_N0001"
EPSILON_IDS = ("E020", "E040")
BASE_IDS = tuple(f"A{index:02d}" for index in range(15))
BENCHMARK_BASE_IDS = ("A00", "A07", "A14")
PROFILE = {
    "relative_orders": (24,),
    "global_nodes": 24,
    "global_residue_nodes": 24,
    "relative_residue_nodes": 20,
    "model_distance": 0.65,
    "relative_quadrature_mode": "collision_scaled_adaptive",
    "relative_adaptive_tolerance": 5.0e-5,
    "relative_adaptive_maximum_intervals": 4096,
}
CENTRAL_TOPOLOGY_IDS = {"A02": "ZN3", "A07": "Z0", "A12": "ZP3"}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5043 = load_module("mts_5043_for_primary24_cost", SCRIPT_5043)
N5030 = M5043.N5030
M5034 = M5043.M5034
ORIGINAL_CATALOG = N5030.chamber_residue_catalog


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def serialized(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def profile_digest() -> str:
    return canonical_digest(
        {
            "marker": MARKER,
            "revision": REVISION,
            "profile": PROFILE,
            "source_5041_sha256": digest(M5043.SCRIPT_5041),
        }
    )


def config() -> dict[str, Any]:
    return M5043.load_config()


def argument_lookup(document: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (str(row["epsilon_id"]), str(row["base_argument_id"])): row
        for row in document["arguments"]
        if row["epsilon_id"] in EPSILON_IDS
    }


def topology_path(
    document: dict[str, Any], event_id: str, epsilon_id: str, base_id: str
) -> Path:
    argument = argument_lookup(document)[(epsilon_id, base_id)]
    names = [f"{event_id}__{argument['argument_id']}.json"]
    alternate = CENTRAL_TOPOLOGY_IDS.get(base_id)
    if alternate is not None:
        names.append(f"{event_id}__{epsilon_id}_{alternate}.json")
    candidates = [
        run / "topologies" / name
        for name in names
        for run in M5043.TOPOLOGY_RUNS
    ]
    existing = [path for path in candidates if path.exists()]
    if not existing:
        raise FileNotFoundError(f"no topology for {epsilon_id} {event_id} {base_id}")
    topology = json.loads(existing[0].read_text(encoding="utf-8"))
    if topology.get("event_id") != event_id:
        raise RuntimeError(f"topology event mismatch: {existing[0]}")
    if not (
        topology.get("assignment_tracking_passed")
        and topology.get("crossing_groups_consistent")
    ):
        raise RuntimeError(f"topology is not validated: {existing[0]}")
    return existing[0]


def output_path(epsilon_id: str, event_id: str, base_id: str) -> Path:
    return RUN / "jobs" / f"{epsilon_id}__{event_id}__{base_id}.json"


def evaluate(
    document: dict[str, Any], event_id: str, epsilon_id: str, base_id: str
) -> dict[str, Any]:
    output = output_path(epsilon_id, event_id, base_id)
    expected_digest = profile_digest()
    if output.exists():
        existing = json.loads(output.read_text(encoding="utf-8"))
        if (
            existing.get("profile_digest") == expected_digest
            and existing.get("status") == "COMPLETED_CONVERGED"
        ):
            return existing
    events = M5043.event_lookup(document)
    arguments = argument_lookup(document)
    event = events[event_id]
    argument = arguments[(epsilon_id, base_id)]
    topology_source = topology_path(document, event_id, epsilon_id, base_id)
    topology = json.loads(topology_source.read_text(encoding="utf-8"))
    target = M5043.complex_value(argument["target_cosine"])
    M5034.configure(event, target)
    M5043.CURRENT_JOB = f"primary24__{epsilon_id}__{event_id}__{base_id}"
    M5043.THEOREM_AUDIT.clear()
    M5043.CHART_AUDIT.clear()
    M5043.NUMERIC_AUDIT.clear()
    started = time.monotonic()
    try:
        gate = N5030.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in PROFILE["relative_orders"]),
            int(PROFILE["global_nodes"]),
            int(PROFILE["global_residue_nodes"]),
            int(PROFILE["relative_residue_nodes"]),
            float(PROFILE["model_distance"]),
            int(document["topology"]["boundary_tracking_steps"]),
            str(PROFILE["relative_quadrature_mode"]),
            float(PROFILE["relative_adaptive_tolerance"]),
            int(PROFILE["relative_adaptive_maximum_intervals"]),
        )
        kernel = M5034.highest_value(gate)
        direct = M5034.KERNEL_MULTIPLIER * kernel
        legacy_job = M5043.primary_job(epsilon_id, event_id, base_id)
        legacy = M5043.complex_value(
            legacy_job["normalized_direct_D_hhh_over_G3"]
        )
        legacy_total, legacy_topology, legacy_source = M5043.source_runtime(legacy_job)
        runtime = time.monotonic() - started
        converged = bool(gate["fixed_event_crossed_integral_converged"])
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "profile": PROFILE,
            "profile_digest": expected_digest,
            "epsilon_id": epsilon_id,
            "event_id": event_id,
            "seed": int(event["seed"]),
            "sample_index": int(event["sample_index"]),
            "base_argument_id": base_id,
            "argument_id": argument["argument_id"],
            "target_cosine": argument["target_cosine"],
            "topology_source": str(topology_source),
            "topology_source_sha256": digest(topology_source),
            "status": "COMPLETED_CONVERGED" if converged else "COMPLETED_UNCONVERGED",
            "raw_fixed_event_kernel": serialized(kernel),
            "normalized_direct_D_hhh_over_G3": serialized(direct),
            "legacy_primary24_direct_D_hhh_over_G3": serialized(legacy),
            "theorem_first_minus_legacy": serialized(direct - legacy),
            "theorem_first_legacy_relative_difference": float(
                abs(direct - legacy) / max(1.0, abs(legacy))
            ),
            "kernel_runtime_seconds": runtime,
            "legacy_job_runtime_seconds": legacy_total,
            "legacy_topology_runtime_seconds": legacy_topology,
            "legacy_kernel_runtime_seconds": legacy_total - legacy_topology,
            "legacy_runtime_source": legacy_source,
            "kernel_runtime_ratio": runtime / max(legacy_total - legacy_topology, 1.0e-12),
            "all_residues_stable": bool(gate["all_residues_stable"]),
            "adaptive_quadrature_converged": all(
                bool(row["adaptive_quadrature_converged"])
                for row in gate["order_rows"]
            ),
            "highest_two_order_relative_residual": float(
                gate["highest_two_order_relative_residual"]
            ),
            "theorem_zero_residue_count": len(M5043.THEOREM_AUDIT),
            "numeric_residue_count": len(M5043.NUMERIC_AUDIT),
            "chart_origin_exclusion_count": len(M5043.CHART_AUDIT),
            "unstable_numeric_residue_count": sum(
                not bool(row["selected_stable"])
                for row in M5043.NUMERIC_AUDIT
            ),
            "valid_for_full_MTS_claim": False,
        }
    except Exception as error:
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "profile": PROFILE,
            "profile_digest": expected_digest,
            "epsilon_id": epsilon_id,
            "event_id": event_id,
            "base_argument_id": base_id,
            "topology_source": str(topology_source),
            "status": "FAILED",
            "error": f"{type(error).__name__}: {error}",
            "kernel_runtime_seconds": time.monotonic() - started,
            "valid_for_full_MTS_claim": False,
        }
    atomic_json(output, result)
    return result


def dry_run(document: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for epsilon_id in EPSILON_IDS:
        for base_id in BASE_IDS:
            topology = topology_path(document, EVENT_ID, epsilon_id, base_id)
            primary = M5043.primary_job(epsilon_id, EVENT_ID, base_id)
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "base_argument_id": base_id,
                    "topology": str(topology),
                    "primary_status": primary["status"],
                }
            )
    result = {
        "event_id": EVENT_ID,
        "expected_jobs": len(rows),
        "all_topologies_exist": all(Path(row["topology"]).exists() for row in rows),
        "all_primary_sources_converged": all(
            row["primary_status"]
            in {"IMPORTED_CONVERGED", "COMPLETED_CONVERGED"}
            for row in rows
        ),
        "rows": rows,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(SOURCE / "dry_run.json", result)
    return result


def run_set(
    document: dict[str, Any], jobs: list[tuple[str, str]], max_wall_seconds: float
) -> list[dict[str, Any]]:
    started = time.monotonic()
    rows = []
    for epsilon_id, base_id in jobs:
        if time.monotonic() - started >= max_wall_seconds:
            break
        print(f"starting {epsilon_id} {EVENT_ID} {base_id}", flush=True)
        row = evaluate(document, EVENT_ID, epsilon_id, base_id)
        rows.append(row)
        print(
            f"finished {epsilon_id} {base_id} status={row['status']} "
            f"seconds={row['kernel_runtime_seconds']:.3f}",
            flush=True,
        )
    return rows


def benchmark(document: dict[str, Any], max_wall_seconds: float) -> dict[str, Any]:
    jobs = [
        (epsilon_id, base_id)
        for epsilon_id in EPSILON_IDS
        for base_id in BENCHMARK_BASE_IDS
    ]
    rows = run_set(document, jobs, max_wall_seconds)
    complete = len(rows) == len(jobs)
    exactness_gate = bool(
        complete
        and all(row["status"] == "COMPLETED_CONVERGED" for row in rows)
        and max(
            float(row.get("theorem_first_legacy_relative_difference", math.inf))
            for row in rows
        )
        < 2.0e-6
    )
    result = {
        "checkpoint_marker": MARKER,
        "event_id": EVENT_ID,
        "jobs": rows,
        "expected_jobs": len(jobs),
        "completed_jobs": len(rows),
        "exactness_gate_threshold": 2.0e-6,
        "maximum_relative_difference": (
            max(
                float(row.get("theorem_first_legacy_relative_difference", math.inf))
                for row in rows
            )
            if rows
            else math.inf
        ),
        "mean_kernel_runtime_ratio": (
            float(np.mean([row["kernel_runtime_ratio"] for row in rows]))
            if rows and all("kernel_runtime_ratio" in row for row in rows)
            else math.inf
        ),
        "exactness_gate_passed": exactness_gate,
        "full_event_run_authorized": exactness_gate,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(BENCHMARK_JSON, result)
    return result


def nonlocal_vector(
    document: dict[str, Any], epsilon_id: str, theorem_first: bool
) -> np.ndarray:
    values = {}
    for base_id in BASE_IDS:
        if theorem_first:
            row = json.loads(
                output_path(epsilon_id, EVENT_ID, base_id).read_text(encoding="utf-8")
            )
            if row.get("status") != "COMPLETED_CONVERGED":
                raise RuntimeError(f"theorem-first row not converged: {epsilon_id} {base_id}")
            value = M5043.complex_value(row["normalized_direct_D_hhh_over_G3"])
        else:
            row = M5043.primary_job(epsilon_id, EVENT_ID, base_id)
            value = M5043.complex_value(row["normalized_direct_D_hhh_over_G3"])
        values[(base_id, "value")] = value
    return M5043.cyclic_nonlocal(document, values)


def analyze(document: dict[str, Any]) -> dict[str, Any]:
    rows = [
        json.loads(output_path(epsilon_id, EVENT_ID, base_id).read_text(encoding="utf-8"))
        for epsilon_id in EPSILON_IDS
        for base_id in BASE_IDS
    ]
    if len(rows) != 30 or not all(
        row.get("status") == "COMPLETED_CONVERGED" for row in rows
    ):
        raise RuntimeError("theorem-first full event is incomplete")
    optimized_kernel = float(sum(row["kernel_runtime_seconds"] for row in rows))
    legacy_kernel = float(sum(row["legacy_kernel_runtime_seconds"] for row in rows))
    topology_cost = float(sum(row["legacy_topology_runtime_seconds"] for row in rows))
    legacy_total = legacy_kernel + topology_cost
    optimized_total = optimized_kernel + topology_cost
    kernel_ratio = optimized_kernel / legacy_kernel
    stored_e020 = nonlocal_vector(document, "E020", False)
    stored_e040 = nonlocal_vector(document, "E040", False)
    optimized_e020 = nonlocal_vector(document, "E020", True)
    optimized_e040 = nonlocal_vector(document, "E040", True)
    stored_richardson = 2.0 * stored_e020 - stored_e040
    optimized_richardson = 2.0 * optimized_e020 - optimized_e040
    vector_relative_difference = float(
        np.linalg.norm(optimized_richardson - stored_richardson)
        / max(1.0, np.linalg.norm(stored_richardson))
    )
    mean_legacy_topology = 2877.069106350014
    mean_legacy_kernel = 3767.0299298999776
    estimated_mean_optimized_high = mean_legacy_topology + kernel_ratio * mean_legacy_kernel
    four_high_hours = 4.0 * estimated_mean_optimized_high / 3600.0
    reserve = json.loads(
        (
            POST
            / "source-intake"
            / "functional_rg"
            / "5044"
            / "symmetric_hybrid_fidelity_gate.json"
        ).read_text(encoding="utf-8")
    )
    reserve_low = float(reserve["selected"]["mean_low_event_cost_seconds"])
    reserve_topology = 1498.156798724996
    reserve_kernel = reserve_low - reserve_topology
    optimized_reserve_low = reserve_topology + kernel_ratio * reserve_kernel
    minimum_high = int(reserve["minimum_high_units"])
    minimum_low = int(reserve["minimum_low_units"])
    repriced_pilot_hours = (
        minimum_high * estimated_mean_optimized_high
        + minimum_low * optimized_reserve_low
    ) / 3600.0
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "jobs": len(rows),
        "theorem_zero_residue_count": sum(
            int(row["theorem_zero_residue_count"]) for row in rows
        ),
        "numeric_residue_count": sum(int(row["numeric_residue_count"]) for row in rows),
        "chart_origin_exclusion_count": sum(
            int(row["chart_origin_exclusion_count"]) for row in rows
        ),
        "maximum_job_relative_difference": max(
            float(row["theorem_first_legacy_relative_difference"]) for row in rows
        ),
        "richardson_vector_relative_difference": vector_relative_difference,
        "legacy_event_topology_seconds": topology_cost,
        "legacy_event_kernel_seconds": legacy_kernel,
        "theorem_first_event_kernel_seconds": optimized_kernel,
        "kernel_runtime_ratio": kernel_ratio,
        "legacy_event_total_seconds": legacy_total,
        "theorem_first_estimated_total_seconds": optimized_total,
        "event_total_runtime_ratio": optimized_total / legacy_total,
        "estimated_mean_optimized_high_event_seconds": estimated_mean_optimized_high,
        "estimated_four_high_unit_hours": four_high_hours,
        "estimated_optimized_reserve_low_event_seconds": optimized_reserve_low,
        "repriced_5044_minimum_pilot_hours": repriced_pilot_hours,
        "four_hour_cap_met_by_four_high_units": four_high_hours <= 4.0,
        "four_hour_cap_met_by_reserve_pilot": repriced_pilot_hours <= 4.0,
        "decision": (
            "ATTACK_TOPOLOGY_COST_NEXT"
            if four_high_hours > 4.0 or repriced_pilot_hours > 4.0
            else "AUTHORIZE_BOUNDED_FRESH_PILOT"
        ),
        "retrospective_cost_repricing_only": True,
        "valid_for_full_MTS_claim": False,
        "formalization_workbench_tree_sha256": M5043.tree_digest(
            POST.parent / "formalization-workbench"
        ),
    }
    atomic_json(RESULT_JSON, result)
    cost_rows = [
        {
            "quantity": key,
            "value": result[key],
        }
        for key in (
            "legacy_event_topology_seconds",
            "legacy_event_kernel_seconds",
            "theorem_first_event_kernel_seconds",
            "kernel_runtime_ratio",
            "legacy_event_total_seconds",
            "theorem_first_estimated_total_seconds",
            "event_total_runtime_ratio",
            "estimated_mean_optimized_high_event_seconds",
            "estimated_four_high_unit_hours",
            "estimated_optimized_reserve_low_event_seconds",
            "repriced_5044_minimum_pilot_hours",
        )
    ]
    COST_CSV.parent.mkdir(parents=True, exist_ok=True)
    with COST_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("quantity", "value"))
        writer.writeheader()
        writer.writerows(cost_rows)
    checks = [
        ("full_event_complete", len(rows) == 30, str(len(rows))),
        ("all_jobs_converged", all(row["status"] == "COMPLETED_CONVERGED" for row in rows), "30 required"),
        ("job_exactness_gate", result["maximum_job_relative_difference"] < 2.0e-6, str(result["maximum_job_relative_difference"])),
        ("vector_exactness_gate", vector_relative_difference < 2.0e-6, str(vector_relative_difference)),
        ("claim_remains_false", not result["valid_for_full_MTS_claim"], "required false"),
        ("formalization_workbench_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
    ]
    validation_rows = [
        {"check": name, "passed": str(passed).lower(), "evidence": evidence}
        for name, passed, evidence in checks
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
        writer.writeheader()
        writer.writerows(validation_rows)
    return result


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "benchmark", "event", "analyze", "all"),
        default="dry-run",
    )
    parser.add_argument("--max-wall-seconds", type=float, default=13_800.0)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    document = config()
    N5030.chamber_residue_catalog = M5043.theorem_first_chamber_residue_catalog
    try:
        if arguments.mode == "dry-run":
            print(json.dumps(dry_run(document), indent=2))
            return
        benchmark_result = None
        if arguments.mode in {"benchmark", "all"}:
            benchmark_result = benchmark(document, arguments.max_wall_seconds)
            print(json.dumps(benchmark_result, indent=2))
            if arguments.mode == "benchmark":
                return
            if not benchmark_result["full_event_run_authorized"]:
                return
        if arguments.mode in {"event", "all"}:
            remaining = [
                (epsilon_id, base_id)
                for epsilon_id in EPSILON_IDS
                for base_id in BASE_IDS
            ]
            rows = run_set(document, remaining, arguments.max_wall_seconds)
            print(
                json.dumps(
                    {
                        "attempted_rows": len(rows),
                        "converged_rows": sum(
                            row["status"] == "COMPLETED_CONVERGED" for row in rows
                        ),
                    },
                    indent=2,
                )
            )
            if arguments.mode == "event":
                return
        if arguments.mode in {"analyze", "all"}:
            result = analyze(document)
            print(json.dumps(result, indent=2))
    finally:
        N5030.chamber_residue_catalog = ORIGINAL_CATALOG


if __name__ == "__main__":
    main()
