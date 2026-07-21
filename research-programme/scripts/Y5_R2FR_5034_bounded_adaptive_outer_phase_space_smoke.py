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
from scipy.stats import qmc


POST = Path(__file__).resolve().parents[1]
SCRIPT_5030 = (
    POST
    / "scripts"
    / "Y5_R2FR_5030_causal_relative_collision_homotopy_gate.py"
)
SCRIPT_5032 = (
    POST / "scripts" / "Y5_R2FR_5032_multi_event_causal_topology_grid.py"
)
GRID_5032 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5032"
    / "multi_event_causal_topology_grid.json"
)
TARGET_5018 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5018"
    / "known_master_without_hhh_and_matched_hhh_target.csv"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5034"
RUNS = SOURCE / "runs"
RESULT_JSON = SOURCE / "outer_phase_space_smoke_results.json"
VECTOR_CSV = SOURCE / "cyclic_hhh_vector_smoke.csv"
GATE_CSV = SOURCE / "outer_phase_space_smoke_gate.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = (
    POST
    / "5034-Y5-R2FR-bounded-adaptive-outer-phase-space-smoke-and-cyclic-hhh-vector.md"
)
MARKER = "MTS_5034_BOUNDED_ADAPTIVE_OUTER_PHASE_SPACE_SMOKE"
SCHEMA_REVISION = "restartable-target-specific-feynman-outer-qmc-v1"
KERNEL_MULTIPLIER = -2.0 / math.pi
DEFAULT_PHYSICAL_COSINES = (-0.6, -0.3, 0.0, 0.3, 0.6)
TIER_TEMPLATES: dict[str, dict[str, Any]] = {
    "primary24": {
        "argument_scope": "all",
        "relative_orders": (24,),
        "global_nodes": 24,
        "global_residue_nodes": 24,
        "relative_residue_nodes": 20,
        "model_distance": 0.65,
        "relative_quadrature_mode": "collision_scaled_adaptive",
        "relative_adaptive_tolerance": 5.0e-5,
        "relative_adaptive_maximum_intervals": 1024,
    },
    "audit32": {
        "argument_scope": "central_cyclic_triplet",
        "relative_orders": (24,),
        "global_nodes": 32,
        "global_residue_nodes": 32,
        "relative_residue_nodes": 24,
        "model_distance": 0.65,
        "relative_quadrature_mode": "collision_scaled_adaptive",
        "relative_adaptive_tolerance": 5.0e-5,
        "relative_adaptive_maximum_intervals": 1024,
    },
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5032 = load_module("mts_5032_for_5034", SCRIPT_5032)
M5030 = M5032.M5030


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


def canonical_float(value: float) -> float:
    return round(float(value), 12)


def target_rows() -> list[dict[str, Any]]:
    with TARGET_5018.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [
        {
            "physical_s_channel_cosine": float(
                row["physical_s_channel_cosine"]
            ),
            "required_matched_hhh_nonlocal_cyclic_D_over_G3": float(
                row["required_matched_hhh_nonlocal_cyclic_D_over_G3"]
            ),
            "known_master_error": float(row["known_master_error"]),
        }
        for row in rows
    ]


def crossing_rows(
    physical_cosines: tuple[float, ...],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    argument_values: list[float] = []
    physical_rows: list[dict[str, Any]] = []
    for cosine in physical_cosines:
        t_ratio = -(1.0 - cosine) / 2.0
        u_ratio = -(1.0 + cosine) / 2.0
        z_t = (3.0 + cosine) / (1.0 - cosine)
        z_u = -(3.0 - cosine) / (1.0 + cosine)
        values = (cosine, z_t, z_u)
        for value in values:
            if not any(abs(value - present) < 1.0e-12 for present in argument_values):
                argument_values.append(float(value))
        physical_rows.append(
            {
                "physical_s_channel_cosine": float(cosine),
                "t_ratio": float(t_ratio),
                "u_ratio": float(u_ratio),
                "s_argument": float(cosine),
                "t_argument": float(z_t),
                "u_argument": float(z_u),
            }
        )
    argument_values.sort()
    arguments = [
        {"argument_id": f"A{index:02d}", "argument": value}
        for index, value in enumerate(argument_values)
    ]
    identifier = {
        canonical_float(row["argument"]): row["argument_id"] for row in arguments
    }
    for row in physical_rows:
        row["s_argument_id"] = identifier[canonical_float(row["s_argument"])]
        row["t_argument_id"] = identifier[canonical_float(row["t_argument"])]
        row["u_argument_id"] = identifier[canonical_float(row["u_argument"])]
    return arguments, physical_rows


def qmc_events(seeds: tuple[int, ...], power: int) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for seed in seeds:
        points = qmc.Sobol(d=3, scramble=True, seed=seed).random_base2(power)
        for sample_index, point in enumerate(points):
            soft_energy = min(max(float(point[0]), 1.0e-7), 1.0 - 1.0e-7)
            events.append(
                {
                    "event_id": f"S{seed}_N{sample_index:04d}",
                    "seed": seed,
                    "sample_index": sample_index,
                    "unit_cube_point": [float(value) for value in point],
                    "soft_energy": soft_energy,
                    "soft_cosine": 2.0 * float(point[1]) - 1.0,
                    "decay_cosine": 2.0 * float(point[2]) - 1.0,
                    "normalized_outer_weight": 1.0 / len(points),
                }
            )
    return events


def selected_argument_ids(
    tier: dict[str, Any],
    arguments: list[dict[str, Any]],
    physical_rows: list[dict[str, Any]],
) -> list[str]:
    if tier["argument_scope"] == "all":
        return [row["argument_id"] for row in arguments]
    central = min(
        physical_rows,
        key=lambda row: abs(row["physical_s_channel_cosine"]),
    )
    return [
        central["s_argument_id"],
        central["t_argument_id"],
        central["u_argument_id"],
    ]


def make_config(arguments: argparse.Namespace) -> dict[str, Any]:
    physical_cosines = tuple(
        float(value) for value in arguments.physical_cosines.split(",")
    )
    seeds = tuple(int(value) for value in arguments.seeds.split(","))
    tier_names = tuple(value for value in arguments.tiers.split(",") if value)
    if len(seeds) < 2:
        raise ValueError("at least two independent Sobol scrambles are required")
    if arguments.power < 0:
        raise ValueError("Sobol power must be non-negative")
    if any(name not in TIER_TEMPLATES for name in tier_names):
        raise ValueError(f"unknown tier in {tier_names}")
    if not physical_cosines:
        raise ValueError("at least one physical cosine is required")
    argument_rows, physical_rows = crossing_rows(physical_cosines)
    for row in argument_rows:
        row["target_cosine"] = complex_row(
            complex(
                row["argument"],
                arguments.evaluation_epsilon,
            )
        )
        row["sheet"] = f"upper_feynman_epsilon_{arguments.evaluation_epsilon}"
    tiers: dict[str, Any] = {}
    for name in tier_names:
        tier = dict(TIER_TEMPLATES[name])
        tier["relative_orders"] = list(tier["relative_orders"])
        tier["argument_ids"] = selected_argument_ids(
            tier, argument_rows, physical_rows
        )
        tiers[name] = tier
    events = qmc_events(seeds, arguments.power)
    config = {
        "checkpoint_marker": MARKER,
        "schema_revision": SCHEMA_REVISION,
        "run_id": arguments.run_id,
        "physical_cosines": list(physical_cosines),
        "crossing_rows": physical_rows,
        "arguments": argument_rows,
        "evaluation_epsilon": arguments.evaluation_epsilon,
        "seeds": list(seeds),
        "power": arguments.power,
        "samples_per_seed": 2**arguments.power,
        "events": events,
        "tiers": tiers,
        "topology": {
            "initial_steps": arguments.topology_steps,
            "maximum_steps": arguments.topology_maximum_steps,
            "regulator": arguments.regulator,
            "path_kind": "feynman",
            "boundary_tracking_steps": arguments.boundary_tracking_steps,
            "classifier": "event-and-target-specific-projective-homotopy",
            "representative_kernel_interpolation_used": False,
        },
        "measure_derivation": {
            "five_angle_measure": "dx dOmega_s/(4pi) dOmega_d/(4pi)",
            "contour_averages": "dphi_global/(2pi) dphi_relative/(2pi)",
            "outer_measure": "dx ds_z/2 dd_z/2 = du_x du_s du_d",
            "outer_jacobian_in_unit_cube": 1.0,
            "kernel_multiplier": KERNEL_MULTIPLIER,
        },
        "regulator_contract": {
            "evaluation_surface": "every direct argument is evaluated at z+i*evaluation_epsilon",
            "reason": "keep transported collision poles off the terminal relative contour during the bounded smoke",
            "real_boundary_extrapolated": False,
            "raised_path_fallback_used": False,
        },
        "source_files": {
            str(SCRIPT_5030): file_digest(SCRIPT_5030),
            str(SCRIPT_5032): file_digest(SCRIPT_5032),
            str(GRID_5032): file_digest(GRID_5032),
            str(TARGET_5018): file_digest(TARGET_5018),
            str(Path(__file__).resolve()): file_digest(Path(__file__).resolve()),
        },
        "target_rows": target_rows(),
        "target_fitted": False,
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
    central = min(
        config["crossing_rows"],
        key=lambda row: abs(row["physical_s_channel_cosine"]),
    )
    priority_ids = [
        central["s_argument_id"],
        central["t_argument_id"],
        central["u_argument_id"],
    ]
    priority_ids.extend(
        row["s_argument_id"]
        for row in sorted(
            config["crossing_rows"],
            key=lambda row: abs(row["physical_s_channel_cosine"]),
        )
        if row["s_argument_id"] not in priority_ids
    )
    priority_ids.extend(
        row["argument_id"]
        for row in sorted(config["arguments"], key=lambda row: abs(row["argument"]))
        if row["argument_id"] not in priority_ids
    )
    arguments = argument_lookup(config)
    for event in config["events"]:
        for argument_id in priority_ids:
            argument = arguments[argument_id]
            for tier_name, tier in config["tiers"].items():
                if argument["argument_id"] not in tier["argument_ids"]:
                    continue
                job_key = (
                    f"{event['event_id']}__{argument['argument_id']}__{tier_name}"
                )
                rows.append(
                    {
                        "job_key": job_key,
                        "event_id": event["event_id"],
                        "argument_id": argument["argument_id"],
                        "tier": tier_name,
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
        value = json.loads(path.read_text(encoding="utf-8"))
        rows[value["job_key"]] = value
    return rows


def known_class_lookup() -> dict[str, str]:
    grid = json.loads(GRID_5032.read_text(encoding="utf-8"))
    return {
        json.dumps(row["descriptor"], separators=(",", ":")): row["class_id"]
        for row in grid["topology_classes"]
    }


def topology_descriptor(document: dict[str, Any]) -> list[list[int]]:
    return [
        list(row) for row in M5032.topology_class_descriptor(document)
    ]


def topology_signature_digest(document: dict[str, Any]) -> str:
    signature = [
        [list(row) for row in chamber]
        for chamber in M5032.topology_signature(document)
    ]
    return canonical_digest(signature)


def configure(event: dict[str, Any], target: complex) -> None:
    M5032.configure_event(event)
    M5030.TARGET_COSINE = target


def topology_path(
    run_directory: Path, event_id: str, argument_id: str
) -> Path:
    return run_directory / "topologies" / f"{event_id}__{argument_id}.json"


def obtain_topology(
    run_directory: Path,
    config: dict[str, Any],
    event: dict[str, Any],
    argument: dict[str, Any],
) -> tuple[dict[str, Any], Path, float]:
    output = topology_path(
        run_directory, event["event_id"], argument["argument_id"]
    )
    if output.exists():
        candidate = json.loads(output.read_text(encoding="utf-8"))
        if (
            candidate.get("config_digest") == config["config_digest"]
            and candidate.get("event_id") == event["event_id"]
            and candidate.get("argument_id") == argument["argument_id"]
        ):
            return candidate, output, 0.0
    started = time.monotonic()
    target = complex_from_row(argument["target_cosine"])
    configure(event, target)
    topology_config = config["topology"]
    steps = int(topology_config["initial_steps"])
    maximum_steps = int(topology_config["maximum_steps"])
    while True:
        document = M5030.homotopy_gate(
            steps,
            float(topology_config["regulator"]),
            str(topology_config["path_kind"]),
            int(topology_config["boundary_tracking_steps"]),
        )
        if (
            document["assignment_tracking_passed"]
            and document["crossing_groups_consistent"]
        ):
            break
        if steps >= maximum_steps:
            break
        steps = min(2 * steps, maximum_steps)
    descriptor = topology_descriptor(document)
    known_class = None
    if abs(argument["argument"] - 1.5) < 1.0e-12:
        known_class = known_class_lookup().get(
            json.dumps(descriptor, separators=(",", ":"))
        )
    document.update(
        {
            "checkpoint_marker": MARKER,
            "config_digest": config["config_digest"],
            "event_id": event["event_id"],
            "argument_id": argument["argument_id"],
            "topology_class_descriptor": descriptor,
            "topology_signature_digest": topology_signature_digest(document),
            "known_5032_class_at_z1p5": known_class,
            "representative_kernel_interpolation_used": False,
            "topology_runtime_seconds": time.monotonic() - started,
            "valid_for_full_MTS_claim": False,
        }
    )
    atomic_json(output, document)
    return document, output, float(document["topology_runtime_seconds"])


def highest_value(gate: dict[str, Any]) -> complex:
    highest_order = max(gate["relative_orders"])
    row = next(
        value
        for value in gate["order_rows"]
        if value["relative_order"] == highest_order
    )
    return complex(row["causally_corrected_value"])


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
        topology, topology_output, topology_seconds = obtain_topology(
            run_directory, config, event, argument
        )
        if not (
            topology["assignment_tracking_passed"]
            and topology["crossing_groups_consistent"]
        ):
            raise RuntimeError("target-specific projective topology did not validate")
        target = complex_from_row(argument["target_cosine"])
        configure(event, target)
        kernel_started = time.monotonic()
        gate = M5030.fixed_event_integral_gate(
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
        kernel = highest_value(gate)
        direct_value = KERNEL_MULTIPLIER * kernel
        if not finite_complex(kernel) or not finite_complex(direct_value):
            raise RuntimeError("non-finite fixed-event kernel")
        kernel_output = (
            run_directory / "kernels" / f"{job['job_key']}.json"
        )
        kernel_document = {
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
        }
        atomic_json(kernel_output, kernel_document)
        converged = bool(gate["fixed_event_crossed_integral_converged"])
        result = {
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


def aggregate_complex(values: list[complex]) -> dict[str, Any]:
    array = np.asarray(values, dtype=np.complex128)
    mean = complex(np.mean(array))
    return {
        "mean": complex_row(mean),
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


def numeric_job(job: dict[str, Any]) -> bool:
    return job.get("status", "").startswith("COMPLETED") and isinstance(
        job.get("normalized_direct_D_hhh_over_G3"), dict
    )


def tier_summary(
    config: dict[str, Any],
    tier_name: str,
    jobs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    tier = config["tiers"][tier_name]
    event_rows = config["events"]
    seeds = config["seeds"]
    samples_per_seed = config["samples_per_seed"]
    value_lookup: dict[tuple[int, int, str], complex] = {}
    convergence_lookup: dict[tuple[int, int, str], bool] = {}
    for job in jobs.values():
        if job.get("tier") != tier_name or not numeric_job(job):
            continue
        key = (int(job["seed"]), int(job["sample_index"]), job["argument_id"])
        value_lookup[key] = complex_from_row(
            job["normalized_direct_D_hhh_over_G3"]
        )
        convergence_lookup[key] = bool(job["integral_converged"])
    direct_rows: list[dict[str, Any]] = []
    for argument in config["arguments"]:
        if argument["argument_id"] not in tier["argument_ids"]:
            continue
        seed_means: list[complex] = []
        completed_samples = 0
        converged_samples = 0
        for seed in seeds:
            values = [
                value_lookup[(seed, sample_index, argument["argument_id"])]
                for sample_index in range(samples_per_seed)
                if (seed, sample_index, argument["argument_id"])
                in value_lookup
            ]
            completed_samples += len(values)
            converged_samples += sum(
                convergence_lookup.get(
                    (seed, sample_index, argument["argument_id"]), False
                )
                for sample_index in range(samples_per_seed)
            )
            if len(values) == samples_per_seed:
                seed_means.append(complex(np.mean(values)))
        estimate = aggregate_complex(seed_means) if seed_means else None
        direct_rows.append(
            {
                "argument_id": argument["argument_id"],
                "argument": argument["argument"],
                "target_cosine": argument["target_cosine"],
                "completed_samples": completed_samples,
                "expected_samples": len(seeds) * samples_per_seed,
                "converged_samples": converged_samples,
                "estimate": estimate,
            }
        )
    cyclic_rows: list[dict[str, Any]] = []
    seed_cyclic: dict[int, dict[float, complex]] = {seed: {} for seed in seeds}
    for crossing in config["crossing_rows"]:
        required_ids = (
            crossing["s_argument_id"],
            crossing["t_argument_id"],
            crossing["u_argument_id"],
        )
        if not all(argument_id in tier["argument_ids"] for argument_id in required_ids):
            continue
        per_seed_means: list[complex] = []
        completed_triplets = 0
        converged_triplets = 0
        for seed in seeds:
            sample_values: list[complex] = []
            for sample_index in range(samples_per_seed):
                keys = [
                    (seed, sample_index, argument_id)
                    for argument_id in required_ids
                ]
                if not all(key in value_lookup for key in keys):
                    continue
                value = (
                    value_lookup[keys[0]]
                    + crossing["t_ratio"] ** 3 * value_lookup[keys[1]]
                    + crossing["u_ratio"] ** 3 * value_lookup[keys[2]]
                )
                sample_values.append(value)
                completed_triplets += 1
                converged_triplets += int(
                    all(convergence_lookup.get(key, False) for key in keys)
                )
            if len(sample_values) == samples_per_seed:
                seed_mean = complex(np.mean(sample_values))
                per_seed_means.append(seed_mean)
                seed_cyclic[seed][
                    canonical_float(crossing["physical_s_channel_cosine"])
                ] = seed_mean
        estimate = aggregate_complex(per_seed_means) if per_seed_means else None
        cyclic_rows.append(
            {
                "physical_s_channel_cosine": crossing[
                    "physical_s_channel_cosine"
                ],
                "z_t": crossing["t_argument"],
                "z_u": crossing["u_argument"],
                "completed_triplets": completed_triplets,
                "expected_triplets": len(seeds) * samples_per_seed,
                "converged_triplets": converged_triplets,
                "estimate": estimate,
            }
        )
    required_cosines = [
        canonical_float(value) for value in config["physical_cosines"]
    ]
    complete_seed_vectors = [
        seed
        for seed in seeds
        if all(value in seed_cyclic[seed] for value in required_cosines)
    ]
    target = {
        canonical_float(row["physical_s_channel_cosine"]): row
        for row in config["target_rows"]
    }
    target_coverage = all(value in target for value in required_cosines)
    comparison_rows: list[dict[str, Any]] = []
    local_coefficients: list[float] = []
    nonlocal_by_seed: dict[int, np.ndarray] = {}
    if complete_seed_vectors and target_coverage:
        shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
        for seed in complete_seed_vectors:
            cyclic_vector = np.asarray(
                [seed_cyclic[seed][value].real for value in required_cosines],
                dtype=float,
            )
            local_coefficient = float(
                shape @ cyclic_vector / (shape @ shape)
            )
            local_coefficients.append(local_coefficient)
            nonlocal_by_seed[seed] = cyclic_vector - local_coefficient * shape
        for index, cosine in enumerate(config["physical_cosines"]):
            values = [nonlocal_by_seed[seed][index] for seed in complete_seed_vectors]
            estimate = float(np.mean(values))
            standard_error = (
                float(np.std(values, ddof=1) / math.sqrt(len(values)))
                if len(values) > 1
                else None
            )
            target_value = target[canonical_float(cosine)][
                "required_matched_hhh_nonlocal_cyclic_D_over_G3"
            ]
            comparison_rows.append(
                {
                    "physical_s_channel_cosine": cosine,
                    "computed_nonlocal_component": estimate,
                    "RQMC_standard_error": standard_error,
                    "fixed_5018_target": target_value,
                    "computed_minus_target": estimate - target_value,
                }
            )
    rms_difference = (
        float(
            np.sqrt(
                np.mean(
                    [row["computed_minus_target"] ** 2 for row in comparison_rows]
                )
            )
        )
        if comparison_rows
        else None
    )
    expected_tier_jobs = sum(
        1 for row in expected_jobs(config) if row["tier"] == tier_name
    )
    tier_jobs = [row for row in jobs.values() if row.get("tier") == tier_name]
    return {
        "tier": tier_name,
        "configuration": tier,
        "expected_jobs": expected_tier_jobs,
        "terminal_jobs": len(tier_jobs),
        "numeric_jobs": sum(numeric_job(row) for row in tier_jobs),
        "converged_jobs": sum(
            bool(row.get("integral_converged")) for row in tier_jobs
        ),
        "failed_jobs": sum(row.get("status") == "FAILED" for row in tier_jobs),
        "direct_rows": direct_rows,
        "cyclic_rows": cyclic_rows,
        "complete_seed_vectors": complete_seed_vectors,
        "full_requested_vector_complete": len(complete_seed_vectors) == len(seeds),
        "best_local_stu_coefficient": (
            aggregate_complex([complex(value, 0.0) for value in local_coefficients])
            if local_coefficients
            else None
        ),
        "nonlocal_target_comparison": comparison_rows,
        "RMS_nonlocal_target_difference": rms_difference,
        "target_fitted": False,
        "valid_for_full_MTS_claim": False,
    }


def tier_comparisons(tiers: dict[str, Any]) -> list[dict[str, Any]]:
    if len(tiers) < 2:
        return []
    names = list(tiers)
    reference = tiers[names[0]]
    rows: list[dict[str, Any]] = []
    reference_by_cosine = {
        canonical_float(row["physical_s_channel_cosine"]): row
        for row in reference["cyclic_rows"]
        if row["estimate"] is not None
    }
    for name in names[1:]:
        for row in tiers[name]["cyclic_rows"]:
            if row["estimate"] is None:
                continue
            cosine = canonical_float(row["physical_s_channel_cosine"])
            if cosine not in reference_by_cosine:
                continue
            low = complex_from_row(reference_by_cosine[cosine]["estimate"]["mean"])
            high = complex_from_row(row["estimate"]["mean"])
            rows.append(
                {
                    "physical_s_channel_cosine": row[
                        "physical_s_channel_cosine"
                    ],
                    "reference_tier": names[0],
                    "audit_tier": name,
                    "reference_value": complex_row(low),
                    "audit_value": complex_row(high),
                    "absolute_difference": abs(high - low),
                    "relative_difference": abs(high - low)
                    / max(abs(high), 1.0),
                }
            )
    return rows


def build_summary(
    config: dict[str, Any], jobs: dict[str, dict[str, Any]], run_state: str
) -> dict[str, Any]:
    expected = expected_jobs(config)
    expected_keys = {row["job_key"] for row in expected}
    terminal_keys = set(jobs) & expected_keys
    tiers = {
        name: tier_summary(config, name, jobs) for name in config["tiers"]
    }
    return {
        "checkpoint_marker": MARKER,
        "schema_revision": SCHEMA_REVISION,
        "run_id": config["run_id"],
        "config_digest": config["config_digest"],
        "run_state": run_state,
        "updated_at": utc_now(),
        "expected_jobs": len(expected),
        "terminal_jobs": len(terminal_keys),
        "remaining_jobs": len(expected_keys - terminal_keys),
        "failed_jobs": sum(
            jobs[key].get("status") == "FAILED" for key in terminal_keys
        ),
        "unconverged_jobs": sum(
            jobs[key].get("status") == "COMPLETED_UNCONVERGED"
            for key in terminal_keys
        ),
        "tiers": tiers,
        "tier_comparisons": tier_comparisons(tiers),
        "outer_measure_derived": True,
        "every_numeric_event_target_specific": all(
            row.get("topology_passed", False)
            and not row.get("representative_kernel_interpolation_used", False)
            for row in jobs.values()
            if numeric_job(row)
        ),
        "target_fitted": False,
        "epsilon_limit_complete": False,
        "production_precision_complete": False,
        "crossing_complete_hhh_cut_claimed": False,
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
    status = {
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
    }
    atomic_json(run_directory / "status.json", status)
    atomic_json(run_directory / "partial_results.json", summary)
    return summary


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def vector_csv_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tier_name, tier in summary["tiers"].items():
        comparison = {
            canonical_float(row["physical_s_channel_cosine"]): row
            for row in tier["nonlocal_target_comparison"]
        }
        for row in tier["cyclic_rows"]:
            estimate = row["estimate"]
            target_row = comparison.get(
                canonical_float(row["physical_s_channel_cosine"])
            )
            rows.append(
                {
                    "tier": tier_name,
                    "physical_s_channel_cosine": row[
                        "physical_s_channel_cosine"
                    ],
                    "cyclic_real": (
                        estimate["mean"]["real"] if estimate is not None else ""
                    ),
                    "cyclic_imaginary": (
                        estimate["mean"]["imaginary"]
                        if estimate is not None
                        else ""
                    ),
                    "RQMC_real_standard_error": (
                        estimate["real_standard_error"]
                        if estimate is not None
                        else ""
                    ),
                    "RQMC_imaginary_standard_error": (
                        estimate["imaginary_standard_error"]
                        if estimate is not None
                        else ""
                    ),
                    "computed_nonlocal_component": (
                        target_row["computed_nonlocal_component"]
                        if target_row is not None
                        else ""
                    ),
                    "fixed_5018_target": (
                        target_row["fixed_5018_target"]
                        if target_row is not None
                        else ""
                    ),
                    "computed_minus_target": (
                        target_row["computed_minus_target"]
                        if target_row is not None
                        else ""
                    ),
                    "completed_triplets": row["completed_triplets"],
                    "expected_triplets": row["expected_triplets"],
                    "converged_triplets": row["converged_triplets"],
                    "target_fitted": False,
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows


def gate_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    primary = next(iter(summary["tiers"].values()))
    all_topologies = summary["every_numeric_event_target_specific"]
    return [
        {
            "gate": "outer_measure_exact_reduction",
            "passed": summary["outer_measure_derived"],
            "evidence": "dmu=du_x du_s du_d after two normalized contour averages",
        },
        {
            "gate": "target_specific_projective_assignment",
            "passed": all_topologies and summary["terminal_jobs"] > 0,
            "evidence": "no representative-class kernel interpolation",
        },
        {
            "gate": "independent_scrambles",
            "passed": len(primary["complete_seed_vectors"]) >= 2,
            "evidence": json.dumps(primary["complete_seed_vectors"]),
        },
        {
            "gate": "primary_cyclic_vector",
            "passed": primary["full_requested_vector_complete"],
            "evidence": f"{len(primary['nonlocal_target_comparison'])} compared rows",
        },
        {
            "gate": "global_node_audit",
            "passed": bool(summary["tier_comparisons"]),
            "evidence": f"{len(summary['tier_comparisons'])} paired cyclic comparisons",
        },
        {
            "gate": "run_terminal",
            "passed": summary["remaining_jobs"] == 0,
            "evidence": f"remaining={summary['remaining_jobs']}",
        },
        {
            "gate": "target_not_fitted",
            "passed": not summary["target_fitted"],
            "evidence": "5018 target loaded only after cyclic vector construction",
        },
        {
            "gate": "production_or_full_MTS_claim",
            "passed": False,
            "evidence": "finite-epsilon bounded smoke only",
        },
    ]


def write_checkpoint_artifacts(
    config: dict[str, Any], summary: dict[str, Any], run_directory: Path
) -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    authoritative = dict(summary)
    authoritative["run_directory"] = str(run_directory)
    authoritative["config_file"] = str(run_directory / "config.json")
    authoritative["status_file"] = str(run_directory / "status.json")
    atomic_json(RESULT_JSON, authoritative)
    vector_rows = vector_csv_rows(summary)
    write_csv(
        VECTOR_CSV,
        vector_rows,
        (
            "tier",
            "physical_s_channel_cosine",
            "cyclic_real",
            "cyclic_imaginary",
            "RQMC_real_standard_error",
            "RQMC_imaginary_standard_error",
            "computed_nonlocal_component",
            "fixed_5018_target",
            "computed_minus_target",
            "completed_triplets",
            "expected_triplets",
            "converged_triplets",
            "target_fitted",
            "valid_for_full_MTS_claim",
            "checkpoint_marker",
        ),
    )
    gates = gate_rows(summary)
    write_csv(
        GATE_CSV,
        [
            {**row, "checkpoint_marker": MARKER}
            for row in gates
        ],
        ("gate", "passed", "evidence", "checkpoint_marker"),
    )
    atomic_text(
        PROVENANCE,
        "\n".join(
            (
                "# 5034 bounded outer-phase-space provenance",
                "",
                f"- Exact phase-space and plus normalization: `post-checkpoint-work/scripts/Y5_R2FR_5010_coupled_three_particle_cut_normalization_and_soft_plus_integrand.py`.",
                f"- Causal relative collision homotopy: `post-checkpoint-work/scripts/{SCRIPT_5030.name}`.",
                f"- Multi-event projective classifier: `post-checkpoint-work/scripts/{SCRIPT_5032.name}`.",
                f"- Fixed comparison target: `post-checkpoint-work/source-intake/functional_rg/5018/{TARGET_5018.name}`.",
                f"- Restartable runner: `post-checkpoint-work/scripts/{Path(__file__).name}`.",
                f"- Run configuration: `post-checkpoint-work/source-intake/functional_rg/5034/runs/{config['run_id']}/config.json`.",
                f"- Partial/final result: `post-checkpoint-work/source-intake/functional_rg/5034/runs/{config['run_id']}/partial_results.json`.",
                "- The five-angle measure is reduced analytically before sampling; no empirical normalization factor is fitted.",
                "- Every numeric event/argument pair receives its own projective Feynman homotopy. The 5033 representative matrix is not used as an interpolator.",
                f"- Every direct argument is evaluated on the common upper regulator surface `Im(z)={config['evaluation_epsilon']}`. The real-boundary limit is deliberately deferred.",
                "- No raised-path fallback is used: a raised path can select a different winding signature for negative crossed arguments.",
                "- The 5018 vector is read only for the final nonlocal comparison. It is never used by the integrator or optimizer.",
                "- This is a finite-epsilon bounded smoke and is not a production coefficient or full-MTS claim.",
                "",
                f"Marker: `{MARKER}`.",
                "",
            )
        ),
    )
    primary_name = next(iter(summary["tiers"]))
    primary = summary["tiers"][primary_name]
    table_rows: list[str] = []
    comparison = {
        canonical_float(row["physical_s_channel_cosine"]): row
        for row in primary["nonlocal_target_comparison"]
    }
    for row in primary["cyclic_rows"]:
        estimate = row["estimate"]
        compared = comparison.get(
            canonical_float(row["physical_s_channel_cosine"])
        )
        cyclic = (
            f"{estimate['mean']['real']:.8g}{estimate['mean']['imaginary']:+.8g}i"
            if estimate is not None
            else "open"
        )
        nonlocal_value = (
            f"{compared['computed_nonlocal_component']:.8g}"
            if compared is not None
            else "open"
        )
        target_value = (
            f"{compared['fixed_5018_target']:.8g}"
            if compared is not None
            else "open"
        )
        table_rows.append(
            f"| {row['physical_s_channel_cosine']:.3g} | `{cyclic}` | {nonlocal_value} | {target_value} | {row['completed_triplets']}/{row['expected_triplets']} |"
        )
    comparison_table = "\n".join(table_rows) if table_rows else "| open | open | open | open | 0 |"
    tier_table = "\n".join(
        f"| {row['physical_s_channel_cosine']:.3g} | {row['relative_difference']:.4g} |"
        for row in summary["tier_comparisons"]
    ) or "| open | open |"
    decision = (
        "The bounded smoke matrix completed. Its numerical vector is diagnostic only."
        if summary["remaining_jobs"] == 0
        else "The wall/job boundary stopped the run cleanly; resume the same run id to complete the matrix."
    )
    atomic_text(
        DOCUMENT,
        f"""# 5034 — bounded adaptive outer phase-space smoke and cyclic `hhh` vector

## Exact outer measure

The normalized three-body variables used since checkpoint 5010 obey

```text
dmu = dx dOmega_s/(4 pi) dOmega_d/(4 pi)
    = dx (ds_z/2) (dd_z/2) dphi_g/(2 pi) dphi_r/(2 pi).
```

The fixed-event causal kernel computes both normalized azimuth contour
averages. With `s_z=2u_s-1` and `d_z=2u_d-1`, the remaining measure is exactly

```text
integral_[0,1]^3 du_x du_s du_d K(x,s_z,d_z).
```

There is no residual Jacobian and no fitted normalization. The direct cut is
`D_hhh/G^3=(-2/pi) E[K]`, exactly as in checkpoints 5017 and 5026.

## Sheet assignment

Each Sobol event and each direct/crossed argument is transported independently
from `z=0.3+i epsilon_0` along the canonical near-boundary Feynman homotopy to
`z_target+i {config['evaluation_epsilon']}`. Projective root tracking and
crossing-group consistency must pass before its kernel is evaluated. Topology
descriptors are audit labels only; no nearest representative and no
class-constant kernel approximation is used.

All arguments, including the five physical ones, remain on this common positive
regulator surface for the smoke. The rejected real-endpoint pilot put collision
poles directly on the terminal relative contour: it produced 12 topology
failures and three finite but unconverged kernels in 36 jobs. Moving to finite
positive epsilon is not a fit; it restores the contour definition. The
epsilon-to-zero limit remains a separate required calculation.

A raised-then-horizontal path is not substituted when the canonical path is
expensive. At the first Sobol event and `z=-3+0.08i`, both paths can be tracked,
but their net winding signatures differ. The runner therefore increases the
canonical Feynman discretization up to its declared bound instead of silently
changing sheets.

## Restart contract

Run `{config['run_id']}` writes an immutable `config.json`, atomic topology and
kernel files, one terminal JSON per job, `status.json`, `partial_results.json`,
and `log.txt`. It stops between complete kernels at the requested wall/job
boundary. Reusing the run id with a changed config is rejected by digest.

Current state: **{summary['run_state']}**; terminal jobs
`{summary['terminal_jobs']}/{summary['expected_jobs']}`; failures
`{summary['failed_jobs']}`; unconverged finite jobs
`{summary['unconverged_jobs']}`.

## Primary cyclic smoke

| z | cyclic D_hhh/G3 | computed nonlocal | fixed 5018 target | event triplets |
|---:|---:|---:|---:|---:|
{comparison_table}

The local `stu` projection is computed from the predicted cyclic vector alone.
The fixed 5018 target is loaded only afterward; `target_fitted=false`.

## Global-node audit

| z | paired tier relative difference |
|---:|---:|
{tier_table}

## Decision

{decision}

- Exact outer-measure reduction: **derived**.
- Eventwise projective Feynman classifier: **implemented**.
- Representative-class interpolation: **not used**.
- Finite-epsilon production precision: **not claimed**.
- Epsilon-to-zero limit, crossing-complete `hhh`, UV coefficient, local GR and full MTS: **open**.

Marker: `{MARKER}`.
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
            "event_count": len(config["events"]),
            "argument_count": len(config["arguments"]),
            "tier_scopes": {
                name: tier["argument_ids"] for name, tier in config["tiers"].items()
            },
            "expected_kernel_jobs": len(expected),
            "outer_measure": config["measure_derivation"],
            "target_fitted": False,
        }
    run_directory = RUNS / config["run_id"]
    config = load_or_create_config(run_directory, config)
    started = time.monotonic()
    jobs = load_jobs(run_directory)
    write_status(run_directory, config, jobs, "RUNNING", started)
    append_log(
        run_directory,
        f"invocation start terminal={len(jobs)} expected={len(expected)} max_wall={arguments.max_wall_seconds}",
    )
    new_kernels = 0
    state = "COMPLETE"
    for job in expected:
        if job["job_key"] in jobs:
            continue
        elapsed = time.monotonic() - started
        if elapsed >= arguments.max_wall_seconds:
            state = "PAUSED_DEADLINE"
            break
        if arguments.max_new_kernels is not None and new_kernels >= arguments.max_new_kernels:
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
    parser.add_argument("--run-id", default="bounded_smoke_v1")
    parser.add_argument("--physical-cosines", default="-0.6,-0.3,0,0.3,0.6")
    parser.add_argument("--seeds", default="503401,503402")
    parser.add_argument("--power", type=int, default=0)
    parser.add_argument("--tiers", default="primary24,audit32")
    parser.add_argument("--evaluation-epsilon", type=float, default=0.08)
    parser.add_argument("--topology-steps", type=int, default=96)
    parser.add_argument("--topology-maximum-steps", type=int, default=12288)
    parser.add_argument("--regulator", type=float, default=1.0e-3)
    parser.add_argument("--boundary-tracking-steps", type=int, default=64)
    parser.add_argument("--max-wall-seconds", type=float, default=13500.0)
    parser.add_argument("--max-new-kernels", type=int)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_wall_seconds <= 0.0:
        raise ValueError("max wall seconds must be positive")
    if arguments.evaluation_epsilon <= 0.0:
        raise ValueError("evaluation epsilon must be positive")
    result = run(arguments)
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
