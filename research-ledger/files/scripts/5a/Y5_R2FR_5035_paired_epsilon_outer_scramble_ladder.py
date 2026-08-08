from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5034 = (
    POST
    / "scripts"
    / "Y5_R2FR_5034_bounded_adaptive_outer_phase_space_smoke.py"
)
SOURCE_5034_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5034"
    / "runs"
    / "bounded_smoke_eps008_v2"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5035"
RUNS = SOURCE / "runs"
RESULT_JSON = SOURCE / "paired_epsilon_ladder_results.json"
LADDER_CSV = SOURCE / "central_epsilon_ladder.csv"
PAIRED_CSV = SOURCE / "paired_epsilon_differences.csv"
AUDIT_CSV = SOURCE / "global_tier_audit.csv"
GATE_CSV = SOURCE / "epsilon_ladder_gate.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
MARKER = "MTS_5035_PAIRED_EPSILON_ZERO_OUTER_SCRAMBLE_LADDER"
SCHEMA_REVISION = "paired-event-central-cyclic-epsilon-ladder-v1"
ARGUMENT_ROWS = (
    ("ZN3", -3.0, -0.125),
    ("Z0", 0.0, 1.0),
    ("ZP3", 3.0, -0.125),
)
TIER_TEMPLATES: dict[str, dict[str, Any]] = {
    "primary24": {
        "relative_orders": (24,),
        "global_nodes": 24,
        "global_residue_nodes": 24,
        "relative_residue_nodes": 20,
        "model_distance": 0.65,
        "relative_quadrature_mode": "collision_scaled_adaptive",
        "relative_adaptive_tolerance": 5.0e-5,
        "relative_adaptive_maximum_intervals": 4096,
    },
    "audit32": {
        "relative_orders": (24,),
        "global_nodes": 32,
        "global_residue_nodes": 32,
        "relative_residue_nodes": 24,
        "model_distance": 0.65,
        "relative_quadrature_mode": "collision_scaled_adaptive",
        "relative_adaptive_tolerance": 5.0e-5,
        "relative_adaptive_maximum_intervals": 4096,
    },
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5034 = load_module("mts_5034_for_5035", SCRIPT_5034)
M5034.MARKER = MARKER


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, indent=2, allow_nan=False) + "\n")


def append_log(run_directory: Path, message: str) -> None:
    run_directory.mkdir(parents=True, exist_ok=True)
    with (run_directory / "log.txt").open("a", encoding="utf-8") as handle:
        handle.write(f"{utc_now()} {message}\n")
        handle.flush()


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def complex_from_row(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


def epsilon_id(value: float) -> str:
    return f"E{round(value * 1000):03d}"


def parse_csv_floats(value: str) -> tuple[float, ...]:
    return tuple(float(item) for item in value.split(",") if item.strip())


def parse_csv_ints(value: str) -> tuple[int, ...]:
    return tuple(int(item) for item in value.split(",") if item.strip())


def make_config(arguments: argparse.Namespace) -> dict[str, Any]:
    epsilons = parse_csv_floats(arguments.epsilons)
    seeds = parse_csv_ints(arguments.seeds)
    if len(epsilons) < 3:
        raise ValueError("at least three positive epsilon levels are required")
    if any(value <= 0.0 for value in epsilons):
        raise ValueError("epsilon levels must be positive")
    if any(left <= right for left, right in zip(epsilons, epsilons[1:])):
        raise ValueError("epsilon levels must be supplied in strictly decreasing order")
    if len(set(epsilon_id(value) for value in epsilons)) != len(epsilons):
        raise ValueError("epsilon labels collide at 0.001 resolution")
    if len(seeds) < 2 or len(set(seeds)) != len(seeds):
        raise ValueError("at least two distinct Sobol scramble seeds are required")
    if arguments.power < 0:
        raise ValueError("Sobol power must be non-negative")
    events = M5034.qmc_events(seeds, arguments.power)
    argument_rows: list[dict[str, Any]] = []
    for epsilon in epsilons:
        label = epsilon_id(epsilon)
        for argument_label, argument_value, cyclic_weight in ARGUMENT_ROWS:
            argument_rows.append(
                {
                    "argument_id": f"{label}_{argument_label}",
                    "epsilon_id": label,
                    "evaluation_epsilon": epsilon,
                    "argument_label": argument_label,
                    "argument": argument_value,
                    "cyclic_weight": cyclic_weight,
                    "target_cosine": complex_row(
                        complex(argument_value, epsilon)
                    ),
                    "sheet": f"upper_feynman_epsilon_{epsilon}",
                }
            )
    tiers = {
        name: {
            **template,
            "relative_orders": list(template["relative_orders"]),
            "seed_scope": (
                "all_scrambles" if name == "primary24" else "first_scramble_only"
            ),
        }
        for name, template in TIER_TEMPLATES.items()
    }
    source_config_path = SOURCE_5034_RUN / "config.json"
    config: dict[str, Any] = {
        "checkpoint_marker": MARKER,
        "schema_revision": SCHEMA_REVISION,
        "run_id": arguments.run_id,
        "epsilons": list(epsilons),
        "epsilon_ids": [epsilon_id(value) for value in epsilons],
        "seeds": list(seeds),
        "audit_seed": seeds[0],
        "power": arguments.power,
        "samples_per_seed": 2**arguments.power,
        "events": events,
        "arguments": argument_rows,
        "tiers": tiers,
        "topology": {
            "initial_steps": arguments.topology_steps,
            "maximum_steps": arguments.topology_maximum_steps,
            "regulator": arguments.regulator,
            "path_kind": "feynman",
            "boundary_tracking_steps": arguments.boundary_tracking_steps,
            "classifier": "event-epsilon-and-argument-specific-projective-homotopy",
            "raised_path_fallback_used": False,
            "representative_kernel_interpolation_used": False,
        },
        "estimator_contract": {
            "central_physical_cosine": 0.0,
            "formula": "C_eps = D(0+i eps) - [D(3+i eps)+D(-3+i eps)]/8",
            "crossing_weights": {
                label: weight for label, _, weight in ARGUMENT_ROWS
            },
            "same_sobol_event_paired_across_epsilon": True,
            "global32_is_quadrature_audit_not_outer_sample": True,
            "target_5018_fitted": False,
        },
        "measure_contract": {
            "outer_domain": "unit cube in (u_x,u_s,u_d)",
            "outer_jacobian": 1.0,
            "fixed_event_multiplier": M5034.KERNEL_MULTIPLIER,
        },
        "reuse_contract": {
            "source_run": str(SOURCE_5034_RUN),
            "source_epsilon": 0.08,
            "reuse_only_exact_event_argument_tier_matches": True,
            "source_config_digest": (
                file_digest(source_config_path) if source_config_path.exists() else None
            ),
        },
        "source_files": {
            str(SCRIPT_5034): file_digest(SCRIPT_5034),
            str(M5034.SCRIPT_5030): file_digest(M5034.SCRIPT_5030),
            str(M5034.SCRIPT_5032): file_digest(M5034.SCRIPT_5032),
            str(M5034.GRID_5032): file_digest(M5034.GRID_5032),
            str(source_config_path): (
                file_digest(source_config_path) if source_config_path.exists() else None
            ),
            str(Path(__file__).resolve()): file_digest(Path(__file__).resolve()),
        },
        "numerical_gate_thresholds": {
            "maximum_global_tier_relative_difference": 1.0e-3,
            "minimum_primary_scrambles": 4,
            "require_contracting_successive_mean_step": True,
        },
        "epsilon_limit_complete": False,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    config["config_digest"] = canonical_digest(config)
    return config


def load_or_create_config(run_directory: Path, config: dict[str, Any]) -> dict[str, Any]:
    path = run_directory / "config.json"
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing.get("config_digest") != config["config_digest"]:
            raise RuntimeError(
                "run configuration changed; use a new run id rather than mixing samples"
            )
        return existing
    run_directory.mkdir(parents=True, exist_ok=True)
    atomic_json(path, config)
    append_log(run_directory, f"created run config {config['config_digest']}")
    return config


def argument_lookup(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["argument_id"]: row for row in config["arguments"]}


def event_lookup(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["event_id"]: row for row in config["events"]}


def expected_jobs(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    arguments = argument_lookup(config)
    ordered_labels = ("Z0", "ZP3", "ZN3")
    for epsilon_label in config["epsilon_ids"]:
        for event in config["events"]:
            for argument_label in ordered_labels:
                argument_id = f"{epsilon_label}_{argument_label}"
                argument = arguments[argument_id]
                rows.append(
                    {
                        "job_key": f"{epsilon_label}__{event['event_id']}__{argument_label}__primary24",
                        "epsilon_id": epsilon_label,
                        "evaluation_epsilon": argument["evaluation_epsilon"],
                        "event_id": event["event_id"],
                        "argument_id": argument_id,
                        "tier": "primary24",
                    }
                )
        audit_event = next(
            row for row in config["events"] if row["seed"] == config["audit_seed"]
        )
        for argument_label in ordered_labels:
            argument_id = f"{epsilon_label}_{argument_label}"
            argument = arguments[argument_id]
            rows.append(
                {
                    "job_key": f"{epsilon_label}__{audit_event['event_id']}__{argument_label}__audit32",
                    "epsilon_id": epsilon_label,
                    "evaluation_epsilon": argument["evaluation_epsilon"],
                    "event_id": audit_event["event_id"],
                    "argument_id": argument_id,
                    "tier": "audit32",
                }
            )
    return rows


def job_path(run_directory: Path, job_key: str) -> Path:
    return run_directory / "jobs" / f"{job_key}.json"


def load_jobs(run_directory: Path) -> dict[str, dict[str, Any]]:
    directory = run_directory / "jobs"
    if not directory.exists():
        return {}
    rows: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        rows[row["job_key"]] = row
    return rows


def source_config_valid(source_config: dict[str, Any]) -> bool:
    supplied = source_config.get("config_digest")
    unsigned = dict(source_config)
    unsigned.pop("config_digest", None)
    return supplied == canonical_digest(unsigned)


def import_reusable_jobs(
    run_directory: Path,
    config: dict[str, Any],
    jobs: dict[str, dict[str, Any]],
) -> int:
    source_config_path = SOURCE_5034_RUN / "config.json"
    source_jobs_directory = SOURCE_5034_RUN / "jobs"
    if not source_config_path.exists() or not source_jobs_directory.exists():
        return 0
    source_config = json.loads(source_config_path.read_text(encoding="utf-8"))
    if not source_config_valid(source_config):
        raise RuntimeError("5034 source config digest does not validate")
    if abs(float(source_config["evaluation_epsilon"]) - 0.08) > 1.0e-15:
        raise RuntimeError("5034 source run is not the locked epsilon=0.08 run")
    source_events = {
        (int(row["seed"]), int(row["sample_index"])): row
        for row in source_config["events"]
    }
    source_arguments = {
        float(row["argument"]): row for row in source_config["arguments"]
    }
    events = event_lookup(config)
    arguments = argument_lookup(config)
    imported = 0
    for expected in expected_jobs(config):
        if expected["job_key"] in jobs:
            continue
        if abs(float(expected["evaluation_epsilon"]) - 0.08) > 1.0e-15:
            continue
        event = events[expected["event_id"]]
        source_event = source_events.get(
            (int(event["seed"]), int(event["sample_index"]))
        )
        if source_event is None:
            continue
        if source_event["unit_cube_point"] != event["unit_cube_point"]:
            raise RuntimeError("Sobol event identity changed across paired runs")
        argument = arguments[expected["argument_id"]]
        source_argument = source_arguments.get(float(argument["argument"]))
        if source_argument is None:
            continue
        source_key = (
            f"{source_event['event_id']}__{source_argument['argument_id']}__{expected['tier']}"
        )
        source_path = source_jobs_directory / f"{source_key}.json"
        if not source_path.exists():
            continue
        source_job = json.loads(source_path.read_text(encoding="utf-8"))
        if (
            source_job.get("config_digest") != source_config["config_digest"]
            or source_job.get("status") != "COMPLETED_CONVERGED"
            or not source_job.get("integral_converged")
            or not source_job.get("topology_passed")
            or abs(float(source_job["target_cosine"]["imaginary"]) - 0.08)
            > 1.0e-15
        ):
            raise RuntimeError(f"source job failed import contract: {source_path}")
        direct = complex_from_row(source_job["normalized_direct_D_hhh_over_G3"])
        raw = complex_from_row(source_job["raw_fixed_event_kernel"])
        if not finite_complex(direct) or not finite_complex(raw):
            raise RuntimeError(f"source job is non-finite: {source_path}")
        result = {
            "checkpoint_marker": MARKER,
            "config_digest": config["config_digest"],
            **expected,
            "seed": event["seed"],
            "sample_index": event["sample_index"],
            "argument": argument["argument"],
            "target_cosine": argument["target_cosine"],
            "status": "IMPORTED_CONVERGED",
            "topology_passed": True,
            "integral_converged": True,
            "representative_kernel_interpolation_used": False,
            "topology_class_descriptor": source_job[
                "topology_class_descriptor"
            ],
            "topology_signature_digest": source_job[
                "topology_signature_digest"
            ],
            "raw_fixed_event_kernel": source_job["raw_fixed_event_kernel"],
            "normalized_direct_D_hhh_over_G3": source_job[
                "normalized_direct_D_hhh_over_G3"
            ],
            "highest_two_order_relative_residual": source_job[
                "highest_two_order_relative_residual"
            ],
            "imported_from": {
                "source_job": str(source_path),
                "source_job_sha256": file_digest(source_path),
                "source_job_key": source_key,
                "source_config": str(source_config_path),
                "source_config_digest": source_config["config_digest"],
            },
            "job_runtime_seconds": 0.0,
            "completed_at": utc_now(),
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(job_path(run_directory, expected["job_key"]), result)
        jobs[expected["job_key"]] = result
        imported += 1
    if imported:
        append_log(run_directory, f"imported {imported} exact-match jobs from 5034")
    return imported


def execute_job(
    run_directory: Path,
    config: dict[str, Any],
    job: dict[str, Any],
) -> dict[str, Any]:
    events = event_lookup(config)
    arguments = argument_lookup(config)
    event = events[job["event_id"]]
    argument = arguments[job["argument_id"]]
    tier = config["tiers"][job["tier"]]
    started = time.monotonic()
    try:
        topology, topology_output, topology_seconds = M5034.obtain_topology(
            run_directory, config, event, argument
        )
        if not (
            topology["assignment_tracking_passed"]
            and topology["crossing_groups_consistent"]
        ):
            raise RuntimeError("target-specific projective topology did not validate")
        target = complex_from_row(argument["target_cosine"])
        M5034.configure(event, target)
        kernel_started = time.monotonic()
        gate = M5034.M5030.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in tier["relative_orders"]),
            int(tier["global_nodes"]),
            int(tier["global_residue_nodes"]),
            int(tier["relative_residue_nodes"]),
            float(tier["model_distance"]),
            int(config["topology"]["boundary_tracking_steps"]),
            str(tier["relative_quadrature_mode"]),
            float(tier["relative_adaptive_tolerance"]),
            int(tier["relative_adaptive_maximum_intervals"]),
        )
        kernel_seconds = time.monotonic() - kernel_started
        kernel = M5034.highest_value(gate)
        direct_value = M5034.KERNEL_MULTIPLIER * kernel
        if not finite_complex(kernel) or not finite_complex(direct_value):
            raise RuntimeError("non-finite fixed-event kernel")
        kernel_output = run_directory / "kernels" / f"{job['job_key']}.json"
        atomic_json(
            kernel_output,
            {
                "checkpoint_marker": MARKER,
                "config_digest": config["config_digest"],
                **job,
                "event": event,
                "argument": argument,
                "topology_file": str(topology_output),
                "topology_class_descriptor": topology[
                    "topology_class_descriptor"
                ],
                "topology_signature_digest": topology[
                    "topology_signature_digest"
                ],
                "fixed_event_integral_gate": gate,
                "valid_for_full_MTS_claim": False,
            },
        )
        converged = bool(gate["fixed_event_crossed_integral_converged"])
        result: dict[str, Any] = {
            "checkpoint_marker": MARKER,
            "config_digest": config["config_digest"],
            **job,
            "seed": event["seed"],
            "sample_index": event["sample_index"],
            "argument": argument["argument"],
            "target_cosine": argument["target_cosine"],
            "status": (
                "COMPLETED_CONVERGED" if converged else "COMPLETED_UNCONVERGED"
            ),
            "topology_passed": True,
            "integral_converged": converged,
            "representative_kernel_interpolation_used": False,
            "topology_class_descriptor": topology[
                "topology_class_descriptor"
            ],
            "topology_signature_digest": topology[
                "topology_signature_digest"
            ],
            "topology_file": str(topology_output),
            "kernel_file": str(kernel_output),
            "raw_fixed_event_kernel": complex_row(kernel),
            "normalized_direct_D_hhh_over_G3": complex_row(direct_value),
            "highest_two_order_relative_residual": gate[
                "highest_two_order_relative_residual"
            ],
            "topology_runtime_seconds": topology_seconds,
            "kernel_runtime_seconds": kernel_seconds,
            "job_runtime_seconds": time.monotonic() - started,
            "completed_at": utc_now(),
            "valid_for_full_MTS_claim": False,
        }
    except Exception as error:
        result = {
            "checkpoint_marker": MARKER,
            "config_digest": config["config_digest"],
            **job,
            "seed": event["seed"],
            "sample_index": event["sample_index"],
            "argument": argument["argument"],
            "target_cosine": argument["target_cosine"],
            "status": "FAILED",
            "error_type": type(error).__name__,
            "error": str(error),
            "job_runtime_seconds": time.monotonic() - started,
            "completed_at": utc_now(),
            "valid_for_full_MTS_claim": False,
        }
    atomic_json(job_path(run_directory, job["job_key"]), result)
    return result


def numeric_job(job: dict[str, Any]) -> bool:
    return (
        job.get("status") in {"COMPLETED_CONVERGED", "IMPORTED_CONVERGED"}
        and bool(job.get("integral_converged"))
        and isinstance(job.get("normalized_direct_D_hhh_over_G3"), dict)
    )


def aggregate_complex(values: list[complex]) -> dict[str, Any]:
    array = np.asarray(values, dtype=np.complex128)
    return {
        "mean": complex_row(complex(np.mean(array))),
        "real_standard_error": (
            float(np.std(array.real, ddof=1) / math.sqrt(len(array)))
            if len(array) > 1
            else None
        ),
        "imaginary_standard_error": (
            float(np.std(array.imag, ddof=1) / math.sqrt(len(array)))
            if len(array) > 1
            else None
        ),
        "replicate_count": len(values),
    }


def cyclic_estimates(
    config: dict[str, Any], jobs: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[tuple[str, str, int], complex]]:
    arguments = argument_lookup(config)
    value_lookup: dict[tuple[str, int, int, str], complex] = {}
    for job in jobs.values():
        if not numeric_job(job):
            continue
        argument = arguments[job["argument_id"]]
        key = (
            job["tier"],
            int(job["seed"]),
            int(job["sample_index"]),
            job["argument_id"],
        )
        value_lookup[key] = complex_from_row(
            job["normalized_direct_D_hhh_over_G3"]
        )
    rows: list[dict[str, Any]] = []
    lookup: dict[tuple[str, str, int], complex] = {}
    for epsilon_label, epsilon in zip(config["epsilon_ids"], config["epsilons"]):
        for tier in config["tiers"]:
            tier_seeds = (
                config["seeds"]
                if tier == "primary24"
                else [config["audit_seed"]]
            )
            for seed in tier_seeds:
                samples: list[complex] = []
                for sample_index in range(config["samples_per_seed"]):
                    terms: list[complex] = []
                    complete = True
                    for argument_label, _, weight in ARGUMENT_ROWS:
                        argument_id = f"{epsilon_label}_{argument_label}"
                        key = (tier, seed, sample_index, argument_id)
                        if key not in value_lookup:
                            complete = False
                            break
                        terms.append(weight * value_lookup[key])
                    if complete:
                        samples.append(sum(terms, start=0j))
                estimate = complex(np.mean(samples)) if samples else None
                if len(samples) == config["samples_per_seed"]:
                    lookup[(tier, epsilon_label, seed)] = estimate
                rows.append(
                    {
                        "epsilon_id": epsilon_label,
                        "epsilon": epsilon,
                        "tier": tier,
                        "seed": seed,
                        "completed_samples": len(samples),
                        "expected_samples": config["samples_per_seed"],
                        "cyclic_value": (
                            complex_row(estimate) if estimate is not None else None
                        ),
                    }
                )
    return rows, lookup


def ladder_rows(
    config: dict[str, Any],
    cyclic_lookup: dict[tuple[str, str, int], complex],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_label, epsilon in zip(config["epsilon_ids"], config["epsilons"]):
        for tier in config["tiers"]:
            seeds = (
                config["seeds"]
                if tier == "primary24"
                else [config["audit_seed"]]
            )
            values = [
                cyclic_lookup[(tier, epsilon_label, seed)]
                for seed in seeds
                if (tier, epsilon_label, seed) in cyclic_lookup
            ]
            rows.append(
                {
                    "epsilon_id": epsilon_label,
                    "epsilon": epsilon,
                    "tier": tier,
                    "completed_scrambles": len(values),
                    "expected_scrambles": len(seeds),
                    "estimate": aggregate_complex(values) if values else None,
                }
            )
    return rows


def paired_rows(
    config: dict[str, Any],
    cyclic_lookup: dict[tuple[str, str, int], complex],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for from_label, to_label, from_epsilon, to_epsilon in zip(
        config["epsilon_ids"],
        config["epsilon_ids"][1:],
        config["epsilons"],
        config["epsilons"][1:],
    ):
        differences: list[complex] = []
        per_seed: list[dict[str, Any]] = []
        for seed in config["seeds"]:
            from_key = ("primary24", from_label, seed)
            to_key = ("primary24", to_label, seed)
            if from_key not in cyclic_lookup or to_key not in cyclic_lookup:
                continue
            difference = cyclic_lookup[to_key] - cyclic_lookup[from_key]
            differences.append(difference)
            per_seed.append(
                {"seed": seed, "difference": complex_row(difference)}
            )
        rows.append(
            {
                "from_epsilon_id": from_label,
                "to_epsilon_id": to_label,
                "from_epsilon": from_epsilon,
                "to_epsilon": to_epsilon,
                "paired_scrambles": len(differences),
                "expected_scrambles": len(config["seeds"]),
                "estimate": aggregate_complex(differences) if differences else None,
                "per_seed": per_seed,
            }
        )
    return rows


def tier_audit_rows(
    config: dict[str, Any],
    cyclic_lookup: dict[tuple[str, str, int], complex],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seed = config["audit_seed"]
    for epsilon_label, epsilon in zip(config["epsilon_ids"], config["epsilons"]):
        primary = cyclic_lookup.get(("primary24", epsilon_label, seed))
        audit = cyclic_lookup.get(("audit32", epsilon_label, seed))
        if primary is None or audit is None:
            rows.append(
                {
                    "epsilon_id": epsilon_label,
                    "epsilon": epsilon,
                    "seed": seed,
                    "complete": False,
                }
            )
            continue
        difference = audit - primary
        rows.append(
            {
                "epsilon_id": epsilon_label,
                "epsilon": epsilon,
                "seed": seed,
                "complete": True,
                "primary24": complex_row(primary),
                "audit32": complex_row(audit),
                "difference": complex_row(difference),
                "absolute_difference": abs(difference),
                "relative_difference": abs(difference) / max(abs(audit), 1.0),
            }
        )
    return rows


def extrapolation_diagnostics(
    config: dict[str, Any],
    ladder: list[dict[str, Any]],
    paired: list[dict[str, Any]],
    cyclic_lookup: dict[tuple[str, str, int], complex],
) -> dict[str, Any]:
    primary = {
        row["epsilon_id"]: row
        for row in ladder
        if row["tier"] == "primary24" and row["estimate"] is not None
    }
    result: dict[str, Any] = {
        "effective_order_defined": False,
        "linear_epsilon_model_tested_not_assumed": True,
        "epsilon_zero_claimed": False,
    }
    if len(config["epsilon_ids"]) >= 3:
        first, second, third = config["epsilon_ids"][:3]
        if all(label in primary for label in (first, second, third)):
            first_value = complex_from_row(primary[first]["estimate"]["mean"])
            second_value = complex_from_row(primary[second]["estimate"]["mean"])
            third_value = complex_from_row(primary[third]["estimate"]["mean"])
            delta_one = second_value - first_value
            delta_two = third_value - second_value
            if abs(delta_one) > 0.0 and abs(delta_two) > 0.0:
                result.update(
                    {
                        "effective_order_defined": True,
                        "effective_order_from_complex_step_norm": math.log(
                            abs(delta_one) / abs(delta_two), 2.0
                        ),
                        "first_mean_step_norm": abs(delta_one),
                        "second_mean_step_norm": abs(delta_two),
                        "successive_mean_step_contracts": abs(delta_two)
                        < abs(delta_one),
                    }
                )
    if len(config["epsilon_ids"]) >= 2:
        larger = config["epsilon_ids"][-2]
        smaller = config["epsilon_ids"][-1]
        ratio = config["epsilons"][-2] / config["epsilons"][-1]
        extrapolated: list[complex] = []
        if abs(ratio - 2.0) < 1.0e-12:
            for seed in config["seeds"]:
                large_key = ("primary24", larger, seed)
                small_key = ("primary24", smaller, seed)
                if large_key in cyclic_lookup and small_key in cyclic_lookup:
                    extrapolated.append(
                        2.0 * cyclic_lookup[small_key] - cyclic_lookup[large_key]
                    )
        if extrapolated:
            result["linear_Richardson_epsilon_zero_diagnostic"] = aggregate_complex(
                extrapolated
            )
            result["linear_Richardson_paired_scrambles"] = len(extrapolated)
    if paired:
        result["paired_step_count"] = len(paired)
    return result


def build_summary(
    config: dict[str, Any], jobs: dict[str, dict[str, Any]], run_state: str
) -> dict[str, Any]:
    expected = expected_jobs(config)
    expected_keys = {row["job_key"] for row in expected}
    terminal_keys = set(jobs) & expected_keys
    cyclic_per_seed, cyclic_lookup = cyclic_estimates(config, jobs)
    ladder = ladder_rows(config, cyclic_lookup)
    paired = paired_rows(config, cyclic_lookup)
    tier_audit = tier_audit_rows(config, cyclic_lookup)
    extrapolation = extrapolation_diagnostics(
        config, ladder, paired, cyclic_lookup
    )
    all_jobs_numeric = len(terminal_keys) == len(expected_keys) and all(
        numeric_job(jobs[key]) for key in expected_keys
    )
    primary_complete = all(
        row["completed_scrambles"] == row["expected_scrambles"]
        for row in ladder
        if row["tier"] == "primary24"
    )
    audit_complete = all(row.get("complete", False) for row in tier_audit)
    tier_threshold = config["numerical_gate_thresholds"][
        "maximum_global_tier_relative_difference"
    ]
    tier_consistent = audit_complete and all(
        row["relative_difference"] <= tier_threshold for row in tier_audit
    )
    scramble_count_sufficient = len(config["seeds"]) >= config[
        "numerical_gate_thresholds"
    ]["minimum_primary_scrambles"]
    contraction = bool(extrapolation.get("successive_mean_step_contracts", False))
    central_extension_gate = (
        all_jobs_numeric
        and primary_complete
        and tier_consistent
        and scramble_count_sufficient
        and contraction
    )
    gate = {
        "all_expected_jobs_numeric_and_converged": all_jobs_numeric,
        "all_primary_epsilon_scrambles_complete": primary_complete,
        "global24_global32_audit_complete": audit_complete,
        "global24_global32_within_threshold": tier_consistent,
        "minimum_four_independent_scrambles": scramble_count_sufficient,
        "successive_mean_epsilon_step_contracts": contraction,
        "central_ladder_allows_full_vector_smoke": central_extension_gate,
        "epsilon_zero_limit_complete": False,
        "production_precision_complete": False,
        "crossing_complete_hhh_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return {
        "checkpoint_marker": MARKER,
        "schema_revision": SCHEMA_REVISION,
        "run_id": config["run_id"],
        "config_digest": config["config_digest"],
        "run_state": run_state,
        "updated_at": utc_now(),
        "expected_jobs": len(expected_keys),
        "terminal_jobs": len(terminal_keys),
        "remaining_jobs": len(expected_keys - terminal_keys),
        "imported_jobs": sum(
            jobs[key].get("status") == "IMPORTED_CONVERGED"
            for key in terminal_keys
        ),
        "computed_jobs": sum(
            jobs[key].get("status") == "COMPLETED_CONVERGED"
            for key in terminal_keys
        ),
        "failed_jobs": sum(
            jobs[key].get("status") == "FAILED" for key in terminal_keys
        ),
        "unconverged_jobs": sum(
            jobs[key].get("status") == "COMPLETED_UNCONVERGED"
            for key in terminal_keys
        ),
        "cyclic_per_seed": cyclic_per_seed,
        "central_epsilon_ladder": ladder,
        "paired_epsilon_differences": paired,
        "global_tier_audit": tier_audit,
        "extrapolation_diagnostics": extrapolation,
        "gate": gate,
        "canonical_feynman_path_only": True,
        "same_events_paired_across_epsilon": True,
        "target_5018_fitted": False,
        "epsilon_limit_complete": False,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def write_status(
    run_directory: Path,
    config: dict[str, Any],
    jobs: dict[str, dict[str, Any]],
    run_state: str,
    started: float,
) -> dict[str, Any]:
    summary = build_summary(config, jobs, run_state)
    atomic_json(
        run_directory / "status.json",
        {
            "checkpoint_marker": MARKER,
            "run_id": config["run_id"],
            "config_digest": config["config_digest"],
            "state": run_state,
            "elapsed_seconds_this_invocation": time.monotonic() - started,
            "expected_jobs": summary["expected_jobs"],
            "terminal_jobs": summary["terminal_jobs"],
            "remaining_jobs": summary["remaining_jobs"],
            "failed_jobs": summary["failed_jobs"],
            "unconverged_jobs": summary["unconverged_jobs"],
            "updated_at": utc_now(),
        },
    )
    atomic_json(run_directory / "partial_results.json", summary)
    return summary


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def write_checkpoint_artifacts(
    config: dict[str, Any], summary: dict[str, Any], run_directory: Path
) -> None:
    atomic_json(RESULT_JSON, summary)
    ladder_rows_csv: list[dict[str, Any]] = []
    for row in summary["central_epsilon_ladder"]:
        estimate = row.get("estimate")
        ladder_rows_csv.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": row["epsilon"],
                "tier": row["tier"],
                "completed_scrambles": row["completed_scrambles"],
                "expected_scrambles": row["expected_scrambles"],
                "mean_real": estimate["mean"]["real"] if estimate else "",
                "mean_imaginary": (
                    estimate["mean"]["imaginary"] if estimate else ""
                ),
                "real_standard_error": (
                    estimate["real_standard_error"] if estimate else ""
                ),
                "imaginary_standard_error": (
                    estimate["imaginary_standard_error"] if estimate else ""
                ),
            }
        )
    write_csv(
        LADDER_CSV,
        ladder_rows_csv,
        [
            "epsilon_id",
            "epsilon",
            "tier",
            "completed_scrambles",
            "expected_scrambles",
            "mean_real",
            "mean_imaginary",
            "real_standard_error",
            "imaginary_standard_error",
        ],
    )
    paired_rows_csv: list[dict[str, Any]] = []
    for row in summary["paired_epsilon_differences"]:
        estimate = row.get("estimate")
        paired_rows_csv.append(
            {
                "from_epsilon": row["from_epsilon"],
                "to_epsilon": row["to_epsilon"],
                "paired_scrambles": row["paired_scrambles"],
                "mean_delta_real": estimate["mean"]["real"] if estimate else "",
                "mean_delta_imaginary": (
                    estimate["mean"]["imaginary"] if estimate else ""
                ),
                "real_standard_error": (
                    estimate["real_standard_error"] if estimate else ""
                ),
                "imaginary_standard_error": (
                    estimate["imaginary_standard_error"] if estimate else ""
                ),
            }
        )
    write_csv(
        PAIRED_CSV,
        paired_rows_csv,
        [
            "from_epsilon",
            "to_epsilon",
            "paired_scrambles",
            "mean_delta_real",
            "mean_delta_imaginary",
            "real_standard_error",
            "imaginary_standard_error",
        ],
    )
    audit_rows_csv = [
        {
            "epsilon": row["epsilon"],
            "seed": row["seed"],
            "complete": row["complete"],
            "absolute_difference": row.get("absolute_difference", ""),
            "relative_difference": row.get("relative_difference", ""),
        }
        for row in summary["global_tier_audit"]
    ]
    write_csv(
        AUDIT_CSV,
        audit_rows_csv,
        [
            "epsilon",
            "seed",
            "complete",
            "absolute_difference",
            "relative_difference",
        ],
    )
    write_csv(
        GATE_CSV,
        [
            {
                "check": check,
                "passed": value,
                "valid_for_full_MTS_claim": False,
            }
            for check, value in summary["gate"].items()
        ],
        ["check", "passed", "valid_for_full_MTS_claim"],
    )
    atomic_text(
        PROVENANCE,
        f"""# 5035 provenance

- Marker: `{MARKER}`.
- Run directory: `{run_directory}`.
- Config digest: `{config['config_digest']}`.
- Numerical parent: `{SCRIPT_5034}` (`{file_digest(SCRIPT_5034)}`).
- Exact-match reuse source: `{SOURCE_5034_RUN}`.
- Paired estimator: `C_eps = D(0+i eps) - (D(3+i eps)+D(-3+i eps))/8`.
- Epsilon levels: `{config['epsilons']}`.
- Sobol scramble seeds: `{config['seeds']}`.
- Every new kernel uses its own canonical projective Feynman homotopy.
- Raised-path fallback and representative-kernel interpolation are forbidden.
- The 5018 target is not fitted or used by this runner.
- This is a central-component convergence smoke, not an epsilon-zero or full-MTS claim.
""",
    )


def run(arguments: argparse.Namespace) -> dict[str, Any]:
    config = make_config(arguments)
    expected = expected_jobs(config)
    if arguments.dry_run:
        return {
            "checkpoint_marker": MARKER,
            "dry_run": True,
            "run_id": config["run_id"],
            "config_digest": config["config_digest"],
            "epsilons": config["epsilons"],
            "seeds": config["seeds"],
            "events": len(config["events"]),
            "expected_jobs": len(expected),
            "expected_primary_jobs": sum(
                row["tier"] == "primary24" for row in expected
            ),
            "expected_audit_jobs": sum(row["tier"] == "audit32" for row in expected),
            "estimator_contract": config["estimator_contract"],
            "valid_for_full_MTS_claim": False,
        }
    run_directory = RUNS / config["run_id"]
    config = load_or_create_config(run_directory, config)
    started = time.monotonic()
    jobs = load_jobs(run_directory)
    imported = import_reusable_jobs(run_directory, config, jobs)
    write_status(run_directory, config, jobs, "RUNNING", started)
    append_log(
        run_directory,
        f"invocation start terminal={len(jobs)} expected={len(expected)} imported={imported} max_wall={arguments.max_wall_seconds}",
    )
    new_kernels = 0
    state = "COMPLETE"
    for job in expected:
        if job["job_key"] in jobs:
            continue
        if time.monotonic() - started >= arguments.max_wall_seconds:
            state = "PAUSED_DEADLINE"
            break
        if (
            arguments.max_new_kernels is not None
            and new_kernels >= arguments.max_new_kernels
        ):
            state = "PAUSED_JOB_LIMIT"
            break
        append_log(run_directory, f"starting {job['job_key']}")
        result = execute_job(run_directory, config, job)
        jobs[job["job_key"]] = result
        new_kernels += 1
        append_log(
            run_directory,
            f"finished {job['job_key']} status={result['status']} seconds={result['job_runtime_seconds']:.3f}",
        )
        write_status(run_directory, config, jobs, "RUNNING", started)
        print(
            json.dumps(
                {
                    "job": job["job_key"],
                    "status": result["status"],
                    "seconds": result["job_runtime_seconds"],
                    "terminal": len(jobs),
                    "expected": len(expected),
                }
            ),
            flush=True,
        )
    if len(set(jobs) & {row["job_key"] for row in expected}) < len(expected):
        if state == "COMPLETE":
            state = "PAUSED"
    summary = write_status(run_directory, config, jobs, state, started)
    if state == "COMPLETE":
        atomic_text(
            run_directory / "COMPLETE",
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "completed_at": utc_now(),
                    "failed_jobs": summary["failed_jobs"],
                    "unconverged_jobs": summary["unconverged_jobs"],
                },
                indent=2,
            )
            + "\n",
        )
    else:
        (run_directory / "COMPLETE").unlink(missing_ok=True)
    append_log(
        run_directory,
        f"invocation stop state={state} terminal={summary['terminal_jobs']} remaining={summary['remaining_jobs']}",
    )
    write_checkpoint_artifacts(config, summary, run_directory)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="central_eps008_004_002_s4_v1")
    parser.add_argument("--epsilons", default="0.08,0.04,0.02")
    parser.add_argument("--seeds", default="503401,503402,503403,503404")
    parser.add_argument("--power", type=int, default=0)
    parser.add_argument("--topology-steps", type=int, default=96)
    parser.add_argument("--topology-maximum-steps", type=int, default=49152)
    parser.add_argument("--regulator", type=float, default=1.0e-3)
    parser.add_argument("--boundary-tracking-steps", type=int, default=64)
    parser.add_argument("--max-wall-seconds", type=float, default=12600.0)
    parser.add_argument("--max-new-kernels", type=int)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_wall_seconds <= 0.0:
        raise ValueError("max wall seconds must be positive")
    result = run(arguments)
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
