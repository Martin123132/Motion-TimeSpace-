from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import statistics
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
MANIFEST = POST / "source-intake" / "functional_rg" / "5076" / "locked_central_anchor_pilot_manifest.json"
HISTORICAL_COSTS = POST / "source-intake" / "functional_rg" / "5075" / "central_anchor_event_costs.csv"
SOURCE = POST / "source-intake" / "functional_rg" / "5078"
RUNS = SOURCE / "runs"
RESULT_JSON = SOURCE / "fresh_central_anchor_topology_cost_smoke.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5078_VALIDATION.csv"
MARKER = "MTS_5078_FRESH_CENTRAL_ANCHOR_TOPOLOGY_COST_SMOKE"
REVISION = "one-fresh-event-all-thirty-topologies-plus-resume-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
CONSTRUCTOR_ALLOWANCE_SECONDS = 0.1
ANCHOR_ID = "A08"
ORDER = (
    "A08",
    "A09",
    "A10",
    "A11",
    "A12",
    "A13",
    "A14",
    "A07",
    "A06",
    "A05",
    "A04",
    "A03",
    "A02",
    "A01",
    "A00",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077 = load_module("mts_5077_for_5078", SCRIPT_5077)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def historical_envelope() -> dict[str, float]:
    with HISTORICAL_COSTS.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    totals = [float(row["projected_high_topology_seconds"]) for row in rows]
    return {
        "event_count": float(len(rows)),
        "minimum_seconds": min(totals),
        "mean_seconds": statistics.fmean(totals),
        "maximum_seconds": max(totals),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-id", default="fresh_central_anchor_topology_smoke_v1"
    )
    arguments = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    config = M5077.make_config(manifest, arguments.run_id)
    run_directory = RUNS / arguments.run_id
    run_directory.mkdir(parents=True, exist_ok=True)
    config_path = run_directory / "config.json"
    if config_path.exists():
        existing_config = json.loads(config_path.read_text(encoding="utf-8"))
        if existing_config["config_digest"] != config["config_digest"]:
            raise RuntimeError("topology smoke config changed; use a new run id")
    else:
        atomic_json(config_path, config)
    seed = int(manifest["fresh_high_scramble_seeds"][0])
    event = next(row for row in config["events"] if int(row["seed"]) == seed)
    event_id = event["event_id"]
    manager = M5077.CentralTopologyManager(run_directory, config)
    previous = (
        json.loads(RESULT_JSON.read_text(encoding="utf-8"))
        if RESULT_JSON.exists()
        and json.loads(RESULT_JSON.read_text(encoding="utf-8")).get("run_id")
        == arguments.run_id
        else {}
    )
    rows: list[dict[str, Any]] = []
    invocation_started = time.monotonic()
    for epsilon_id in ("E040", "E020"):
        for base_id in ORDER:
            argument_id = f"{epsilon_id}_{base_id}"
            expected_path = manager.output_path(event_id, argument_id)
            existed_before = expected_path.exists()
            started = time.monotonic()
            document, output, measured_runtime = manager.obtain(
                event_id, epsilon_id, base_id
            )
            invocation_seconds = time.monotonic() - started
            metadata_valid = (
                output.exists()
                and document.get("config_digest") == config["config_digest"]
                and document.get("event_id") == event_id
                and document.get("argument_id") == argument_id
            )
            method = (
                "full_anchor"
                if epsilon_id == "E040" and base_id == ANCHOR_ID
                else "argument_composition"
                if epsilon_id == "E040"
                else "epsilon_composition"
            )
            rows.append(
                {
                    "event_id": event_id,
                    "epsilon_id": epsilon_id,
                    "base_argument_id": base_id,
                    "argument_id": argument_id,
                    "method": method,
                    "existed_before": existed_before,
                    "created_this_invocation": not existed_before and output.exists(),
                    "resumed_from_cache": existed_before and measured_runtime == 0.0,
                    "measured_topology_runtime_seconds": measured_runtime,
                    "invocation_seconds": invocation_seconds,
                    "metadata_valid": metadata_valid,
                    "topology_path": str(output),
                }
            )
            print(
                json.dumps(
                    {
                        "argument": argument_id,
                        "method": method,
                        "seconds": measured_runtime,
                        "resumed": existed_before and measured_runtime == 0.0,
                    }
                ),
                flush=True,
            )
    invocation_seconds = time.monotonic() - invocation_started
    created_count = sum(bool(row["created_this_invocation"]) for row in rows)
    resumed_count = sum(bool(row["resumed_from_cache"]) for row in rows)
    measured_seconds = sum(
        float(row["measured_topology_runtime_seconds"]) for row in rows
    )
    if created_count:
        write_rows(SOURCE / "fresh_topology_rows.csv", rows)
    else:
        write_rows(SOURCE / "resume_topology_rows.csv", rows)
    first_fresh_seconds = previous.get("first_fresh_measured_seconds")
    first_fresh_with_allowance = previous.get(
        "first_fresh_projected_seconds_with_constructor_allowance"
    )
    if first_fresh_seconds is None and created_count == 30:
        first_fresh_seconds = measured_seconds
        first_fresh_with_allowance = (
            measured_seconds + 29 * CONSTRUCTOR_ALLOWANCE_SECONDS
        )
    envelope = historical_envelope()
    envelope_supported = bool(
        first_fresh_with_allowance is not None
        and first_fresh_with_allowance <= envelope["maximum_seconds"]
    )
    cumulative_created = int(previous.get("cumulative_created_count", 0)) + created_count
    cumulative_resumed = int(previous.get("cumulative_resumed_count", 0)) + resumed_count
    structural_passed = (
        len(rows) == 30
        and all(bool(row["metadata_valid"]) for row in rows)
        and sum(row["method"] == "full_anchor" for row in rows) == 1
        and sum(row["method"] == "argument_composition" for row in rows) == 14
        and sum(row["method"] == "epsilon_composition" for row in rows) == 15
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": arguments.run_id,
        "event_id": event_id,
        "seed": seed,
        "artifact_count": len(rows),
        "created_this_invocation_count": created_count,
        "resumed_this_invocation_count": resumed_count,
        "cumulative_created_count": cumulative_created,
        "cumulative_resumed_count": cumulative_resumed,
        "invocation_seconds": invocation_seconds,
        "measured_seconds_this_invocation": measured_seconds,
        "first_fresh_measured_seconds": first_fresh_seconds,
        "constructor_allowance_seconds": 29
        * CONSTRUCTOR_ALLOWANCE_SECONDS,
        "first_fresh_projected_seconds_with_constructor_allowance": first_fresh_with_allowance,
        "historical_projected_topology_minimum_seconds": envelope[
            "minimum_seconds"
        ],
        "historical_projected_topology_mean_seconds": envelope["mean_seconds"],
        "historical_projected_topology_maximum_seconds": envelope[
            "maximum_seconds"
        ],
        "fresh_to_historical_mean_ratio": first_fresh_with_allowance
        / envelope["mean_seconds"]
        if first_fresh_with_allowance is not None
        else None,
        "fresh_to_historical_maximum_ratio": first_fresh_with_allowance
        / envelope["maximum_seconds"]
        if first_fresh_with_allowance is not None
        else None,
        "fresh_topology_structure_passed": structural_passed,
        "resume_contract_exercised": cumulative_resumed >= 30,
        "historical_topology_cost_envelope_supported": envelope_supported,
        "pilot_cost_model_supported_by_one_fresh_event": envelope_supported
        and structural_passed,
        "fresh_kernel_execution_started": False,
        "pilot_execution_authorized": False,
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        (
            "source_paths_exist",
            all(path.exists() for path in (SCRIPT_5077, MANIFEST, HISTORICAL_COSTS)),
            "runner, manifest, and historical cost rows exist",
        ),
        (
            "manifest_locked",
            bool(manifest["statistical_design_locked"]),
            "5076 statistical design remains locked",
        ),
        (
            "thirty_topologies",
            result["artifact_count"] == 30,
            f"artifacts={result['artifact_count']}",
        ),
        (
            "topology_structure",
            result["fresh_topology_structure_passed"],
            "one full anchor, fourteen argument constructions, fifteen epsilon constructions",
        ),
        (
            "fresh_invocation_recorded",
            result["cumulative_created_count"] >= 30,
            f"created={result['cumulative_created_count']}",
        ),
        (
            "resume_state_consistent",
            result["resume_contract_exercised"]
            == (result["cumulative_resumed_count"] >= 30),
            f"resumed={result['cumulative_resumed_count']}",
        ),
        (
            "cost_decision_consistent",
            result["pilot_cost_model_supported_by_one_fresh_event"]
            == (
                result["historical_topology_cost_envelope_supported"]
                and result["fresh_topology_structure_passed"]
            ),
            f"fresh/max={result['fresh_to_historical_maximum_ratio']}",
        ),
        (
            "no_kernel_execution",
            not result["fresh_kernel_execution_started"],
            "5078 constructs topology documents only",
        ),
        (
            "full_pilot_blocked",
            not result["pilot_execution_authorized"],
            "one fresh event cannot authorize the full pilot",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "runtime validation is not physical evidence",
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
                    "check_id": f"V5078_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5078 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
