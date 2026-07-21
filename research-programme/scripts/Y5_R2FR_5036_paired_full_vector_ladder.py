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
SCRIPT_5035_REPAIR = (
    POST / "scripts" / "Y5_R2FR_5035_pair_local_residue_radius_repair.py"
)
SOURCE_5034_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5034"
    / "runs"
    / "bounded_smoke_eps008_v2"
)
SOURCE_5034_REPAIR = (
    SOURCE_5034_RUN
    / "repairs"
    / "S503401_N0000__A00__primary24"
    / "job.json"
)
SOURCE_5035_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5035"
    / "runs"
    / "central_eps008_004_002_s4_v1"
)
SOURCE_5035_REPAIR = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5035"
    / "repairs"
    / "pair_local_shrinking_radius_v1"
    / "repair_summary.json"
)
TARGET_5018 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5018"
    / "known_master_without_hhh_and_matched_hhh_target.csv"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5036"
RUNS = SOURCE / "runs"
RESULT_JSON = SOURCE / "paired_full_vector_results.json"
VECTOR_CSV = SOURCE / "epsilon_cyclic_vector.csv"
DECOMPOSITION_CSV = SOURCE / "local_nonlocal_decomposition.csv"
PAIRED_CSV = SOURCE / "paired_vector_convergence.csv"
TARGET_CSV = SOURCE / "epsilon_zero_target_comparison.csv"
GATE_CSV = SOURCE / "full_vector_ladder_gate.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
MARKER = "MTS_5036_PAIRED_EPSILON_FULL_CYCLIC_VECTOR"
SCHEMA_REVISION = "paired-event-full-cyclic-vector-shrinking-residue-v1"
DEFAULT_PHYSICAL_COSINES = (-0.6, -0.3, 0.0, 0.3, 0.6)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


MREPAIR = load_module("mts_5035_radius_repair_for_5036", SCRIPT_5035_REPAIR)
M5035 = MREPAIR.M5035
N5030 = MREPAIR.N5030
ORIGINAL_CATALOG = N5030.chamber_residue_catalog
M5035.MARKER = MARKER
M5035.M5034.MARKER = MARKER


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


def canonical_float(value: float) -> float:
    return round(float(value), 12)


def parse_csv_floats(value: str) -> tuple[float, ...]:
    return tuple(float(item) for item in value.split(",") if item.strip())


def parse_csv_ints(value: str) -> tuple[int, ...]:
    return tuple(int(item) for item in value.split(",") if item.strip())


def source_config_valid(config: dict[str, Any]) -> bool:
    supplied = config.get("config_digest")
    unsigned = dict(config)
    unsigned.pop("config_digest", None)
    return supplied == canonical_digest(unsigned)


def make_config(arguments: argparse.Namespace) -> dict[str, Any]:
    epsilons = parse_csv_floats(arguments.epsilons)
    seeds = parse_csv_ints(arguments.seeds)
    physical_cosines = parse_csv_floats(arguments.physical_cosines)
    if len(epsilons) < 3 or any(value <= 0.0 for value in epsilons):
        raise ValueError("at least three positive epsilon levels are required")
    if any(left <= right for left, right in zip(epsilons, epsilons[1:])):
        raise ValueError("epsilon levels must be strictly decreasing")
    if len(seeds) < 2 or len(set(seeds)) != len(seeds):
        raise ValueError("at least two distinct Sobol scrambles are required")
    if tuple(physical_cosines) != DEFAULT_PHYSICAL_COSINES:
        raise ValueError("5036 locks the five 5018 physical cosine rows")
    if arguments.power < 0:
        raise ValueError("Sobol power must be non-negative")
    base_arguments, crossings = M5035.M5034.crossing_rows(physical_cosines)
    arguments_flat: list[dict[str, Any]] = []
    for epsilon in epsilons:
        label = epsilon_id(epsilon)
        for base in base_arguments:
            arguments_flat.append(
                {
                    "argument_id": f"{label}_{base['argument_id']}",
                    "base_argument_id": base["argument_id"],
                    "epsilon_id": label,
                    "evaluation_epsilon": epsilon,
                    "argument": base["argument"],
                    "target_cosine": complex_row(
                        complex(base["argument"], epsilon)
                    ),
                    "sheet": f"upper_feynman_epsilon_{epsilon}",
                }
            )
    tiers = {
        name: {
            **template,
            "relative_orders": list(template["relative_orders"]),
            "argument_scope": (
                "all_fifteen" if name == "primary24" else "central_triplet"
            ),
            "seed_scope": (
                "all_scrambles" if name == "primary24" else "first_scramble_only"
            ),
            "residue_radius_revision": MREPAIR.REVISION,
        }
        for name, template in TIER_TEMPLATES.items()
    }
    source_5034_config = SOURCE_5034_RUN / "config.json"
    source_5035_config = SOURCE_5035_RUN / "config.json"
    config: dict[str, Any] = {
        "checkpoint_marker": MARKER,
        "schema_revision": SCHEMA_REVISION,
        "run_id": arguments.run_id,
        "physical_cosines": list(physical_cosines),
        "epsilons": list(epsilons),
        "epsilon_ids": [epsilon_id(value) for value in epsilons],
        "seeds": list(seeds),
        "audit_seed": seeds[0],
        "power": arguments.power,
        "samples_per_seed": 2**arguments.power,
        "events": M5035.M5034.qmc_events(seeds, arguments.power),
        "base_arguments": base_arguments,
        "arguments": arguments_flat,
        "crossings": crossings,
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
        "full_vector_contract": {
            "cyclic_formula": "C(z)=D(z)+(t/s)^3 D(z_t)+(u/s)^3 D(z_u)",
            "local_shape": "phi(z)=1-z^2",
            "eventwise_local_projection": "a=(phi dot C)/(phi dot phi)",
            "eventwise_nonlocal_residual": "R=C-a phi; phi dot R=0",
            "same_sobol_events_paired_across_epsilon": True,
            "decomposition_before_target_comparison": True,
            "target_fitted": False,
        },
        "residue_radius_contract": {
            "revision": MREPAIR.REVISION,
            "candidate_fractions": list(MREPAIR.CANDIDATE_FRACTIONS),
            "selection": "first stable nested pair while shrinking from 0.1; 0.2 diagnostic last",
            "applied_to_every_new_kernel": True,
        },
        "source_reuse": {
            "epsilon_0p08_full_matrix": str(SOURCE_5034_RUN),
            "epsilon_0p08_extreme_repair": str(SOURCE_5034_REPAIR),
            "central_epsilon_ladder": str(SOURCE_5035_RUN),
            "central_residue_repair": str(SOURCE_5035_REPAIR),
            "exact_event_argument_epsilon_tier_match_required": True,
        },
        "source_files": {
            str(M5035.M5034.SCRIPT_5030): file_digest(M5035.M5034.SCRIPT_5030),
            str(M5035.M5034.SCRIPT_5032): file_digest(M5035.M5034.SCRIPT_5032),
            str(M5035.SCRIPT_5034): file_digest(M5035.SCRIPT_5034),
            str(MREPAIR.SCRIPT_5035): file_digest(MREPAIR.SCRIPT_5035),
            str(SCRIPT_5035_REPAIR): file_digest(SCRIPT_5035_REPAIR),
            str(source_5034_config): file_digest(source_5034_config),
            str(SOURCE_5034_REPAIR): file_digest(SOURCE_5034_REPAIR),
            str(source_5035_config): file_digest(source_5035_config),
            str(SOURCE_5035_REPAIR): file_digest(SOURCE_5035_REPAIR),
            str(TARGET_5018): file_digest(TARGET_5018),
            str(Path(__file__).resolve()): file_digest(Path(__file__).resolve()),
        },
        "target_rows": M5035.M5034.target_rows(),
        "numerical_gate_thresholds": {
            "maximum_global_tier_relative_difference": 1.0e-3,
            "maximum_projection_orthogonality_residual": 1.0e-9,
        },
        "target_fitted": False,
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
                "run configuration changed; use a new run id rather than mixing jobs"
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


def ordered_base_argument_ids(config: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for crossing in sorted(
        config["crossings"],
        key=lambda row: abs(row["physical_s_channel_cosine"]),
    ):
        for key in ("s_argument_id", "t_argument_id", "u_argument_id"):
            value = crossing[key]
            if value not in values:
                values.append(value)
    for row in config["base_arguments"]:
        if row["argument_id"] not in values:
            values.append(row["argument_id"])
    return values


def expected_jobs(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base_order = ordered_base_argument_ids(config)
    central = min(
        config["crossings"],
        key=lambda row: abs(row["physical_s_channel_cosine"]),
    )
    central_ids = (
        central["s_argument_id"],
        central["t_argument_id"],
        central["u_argument_id"],
    )
    for epsilon_label, epsilon in zip(config["epsilon_ids"], config["epsilons"]):
        for event in config["events"]:
            for base_id in base_order:
                argument_id = f"{epsilon_label}_{base_id}"
                rows.append(
                    {
                        "job_key": f"{epsilon_label}__{event['event_id']}__{base_id}__primary24",
                        "epsilon_id": epsilon_label,
                        "evaluation_epsilon": epsilon,
                        "event_id": event["event_id"],
                        "argument_id": argument_id,
                        "base_argument_id": base_id,
                        "tier": "primary24",
                    }
                )
        audit_event = next(
            row for row in config["events"] if row["seed"] == config["audit_seed"]
        )
        for base_id in central_ids:
            argument_id = f"{epsilon_label}_{base_id}"
            rows.append(
                {
                    "job_key": f"{epsilon_label}__{audit_event['event_id']}__{base_id}__audit32",
                    "epsilon_id": epsilon_label,
                    "evaluation_epsilon": epsilon,
                    "event_id": audit_event["event_id"],
                    "argument_id": argument_id,
                    "base_argument_id": base_id,
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


def source_key(job: dict[str, Any]) -> tuple[float, int, int, float, str]:
    return (
        canonical_float(job["target_cosine"]["imaginary"]),
        int(job["seed"]),
        int(job["sample_index"]),
        canonical_float(job["argument"]),
        str(job["tier"]),
    )


def source_job_map(
    source_run: Path,
    source_label: str,
    extra_jobs: tuple[Path, ...] = (),
) -> tuple[
    dict[tuple[float, int, int, float, str], tuple[dict[str, Any], Path, str]],
    dict[tuple[int, int], list[float]],
]:
    config_path = source_run / "config.json"
    source_config = json.loads(config_path.read_text(encoding="utf-8"))
    if not source_config_valid(source_config):
        raise RuntimeError(f"source config digest failed: {config_path}")
    event_points = {
        (int(row["seed"]), int(row["sample_index"])): row["unit_cube_point"]
        for row in source_config["events"]
    }
    mapping: dict[
        tuple[float, int, int, float, str], tuple[dict[str, Any], Path, str]
    ] = {}
    paths = list(sorted((source_run / "jobs").glob("*.json"))) + list(extra_jobs)
    for path in paths:
        row = json.loads(path.read_text(encoding="utf-8"))
        if (
            row.get("status") not in {"COMPLETED_CONVERGED", "IMPORTED_CONVERGED"}
            or not row.get("integral_converged")
            or not row.get("topology_passed")
            or not isinstance(row.get("normalized_direct_D_hhh_over_G3"), dict)
        ):
            continue
        mapping[source_key(row)] = (row, path, source_label)
    return mapping, event_points


def import_reusable_jobs(
    run_directory: Path,
    config: dict[str, Any],
    jobs: dict[str, dict[str, Any]],
) -> dict[str, int]:
    map_5034, events_5034 = source_job_map(
        SOURCE_5034_RUN, "5034_epsilon_0p08_full", (SOURCE_5034_REPAIR,)
    )
    map_5035, events_5035 = source_job_map(
        SOURCE_5035_RUN, "5035_central_epsilon_ladder"
    )
    events = event_lookup(config)
    arguments = argument_lookup(config)
    imported_counts = {
        "5034_epsilon_0p08_full": 0,
        "5035_central_epsilon_ladder": 0,
    }
    for expected in expected_jobs(config):
        if expected["job_key"] in jobs:
            continue
        event = events[expected["event_id"]]
        argument = arguments[expected["argument_id"]]
        key = (
            canonical_float(expected["evaluation_epsilon"]),
            int(event["seed"]),
            int(event["sample_index"]),
            canonical_float(argument["argument"]),
            expected["tier"],
        )
        source_entry = map_5034.get(key) if key[0] == 0.08 else map_5035.get(key)
        if source_entry is None:
            continue
        source_job, source_path, source_label = source_entry
        source_events = events_5034 if source_label.startswith("5034") else events_5035
        point = source_events.get((int(event["seed"]), int(event["sample_index"])))
        if point != event["unit_cube_point"]:
            raise RuntimeError(f"paired Sobol event mismatch for {expected['job_key']}")
        direct = complex_from_row(source_job["normalized_direct_D_hhh_over_G3"])
        if not finite_complex(direct):
            raise RuntimeError(f"non-finite source job {source_path}")
        result: dict[str, Any] = {
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
                "source_label": source_label,
                "source_job": str(source_path),
                "source_job_sha256": file_digest(source_path),
                "source_job_key": source_job["job_key"],
            },
            "upstream_repair_contract": source_job.get("repair_contract"),
            "job_runtime_seconds": 0.0,
            "completed_at": utc_now(),
            "valid_for_full_MTS_claim": False,
        }
        atomic_json(job_path(run_directory, expected["job_key"]), result)
        jobs[expected["job_key"]] = result
        imported_counts[source_label] += 1
    if sum(imported_counts.values()):
        append_log(run_directory, f"exact imports {imported_counts}")
    return imported_counts


def execute_new_job(
    run_directory: Path,
    config: dict[str, Any],
    job: dict[str, Any],
) -> dict[str, Any]:
    MREPAIR.CURRENT_JOB = job["job_key"]
    MREPAIR.RADIUS_AUDIT.clear()
    result = M5035.execute_job(run_directory, config, job)
    if result.get("status", "").startswith("COMPLETED"):
        kernel_path = run_directory / "kernels" / f"{job['job_key']}.json"
        kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
        adjustments = list(MREPAIR.RADIUS_AUDIT)
        radius_contract = {
            "revision": MREPAIR.REVISION,
            "candidate_fractions": list(MREPAIR.CANDIDATE_FRACTIONS),
            "adjustment_count": len(adjustments),
            "adjustments": adjustments,
            "repair_script": str(SCRIPT_5035_REPAIR),
            "repair_script_sha256": file_digest(SCRIPT_5035_REPAIR),
            "valid_for_full_MTS_claim": False,
        }
        kernel["fixed_event_integral_gate"]["relative_residue_revision"] = (
            MREPAIR.REVISION
        )
        kernel["residue_radius_contract"] = radius_contract
        result["residue_radius_contract"] = radius_contract
        atomic_json(kernel_path, kernel)
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


def cyclic_seed_vectors(
    config: dict[str, Any], jobs: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[tuple[str, str, int], np.ndarray]]:
    values: dict[tuple[str, int, int, str], complex] = {}
    for job in jobs.values():
        if numeric_job(job):
            values[
                (
                    job["tier"],
                    int(job["seed"]),
                    int(job["sample_index"]),
                    job["argument_id"],
                )
            ] = complex_from_row(job["normalized_direct_D_hhh_over_G3"])
    rows: list[dict[str, Any]] = []
    lookup: dict[tuple[str, str, int], np.ndarray] = {}
    for epsilon_label, epsilon in zip(config["epsilon_ids"], config["epsilons"]):
        for tier in ("primary24",):
            seeds = config["seeds"]
            for seed in seeds:
                sample_vectors: list[np.ndarray] = []
                for sample_index in range(config["samples_per_seed"]):
                    components: list[complex] = []
                    complete = True
                    for crossing in config["crossings"]:
                        ids = [
                            f"{epsilon_label}_{crossing['s_argument_id']}",
                            f"{epsilon_label}_{crossing['t_argument_id']}",
                            f"{epsilon_label}_{crossing['u_argument_id']}",
                        ]
                        keys = [(tier, seed, sample_index, value) for value in ids]
                        if not all(key in values for key in keys):
                            complete = False
                            break
                        components.append(
                            values[keys[0]]
                            + crossing["t_ratio"] ** 3 * values[keys[1]]
                            + crossing["u_ratio"] ** 3 * values[keys[2]]
                        )
                    if complete:
                        sample_vectors.append(
                            np.asarray(components, dtype=np.complex128)
                        )
                vector = (
                    np.mean(np.stack(sample_vectors), axis=0)
                    if sample_vectors
                    else None
                )
                if len(sample_vectors) == config["samples_per_seed"]:
                    lookup[(tier, epsilon_label, seed)] = vector
                rows.append(
                    {
                        "epsilon_id": epsilon_label,
                        "epsilon": epsilon,
                        "tier": tier,
                        "seed": seed,
                        "completed_samples": len(sample_vectors),
                        "expected_samples": config["samples_per_seed"],
                        "cyclic_vector": (
                            [complex_row(complex(value)) for value in vector]
                            if vector is not None
                            else None
                        ),
                    }
                )
    return rows, lookup


def project_vector(
    vector: np.ndarray, shape: np.ndarray
) -> tuple[complex, np.ndarray, float]:
    coefficient = complex(shape @ vector / (shape @ shape))
    residual = vector - coefficient * shape
    orthogonality = float(abs(shape @ residual))
    return coefficient, residual, orthogonality


def vector_summaries(
    config: dict[str, Any],
    lookup: dict[tuple[str, str, int], np.ndarray],
) -> list[dict[str, Any]]:
    shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
    rows: list[dict[str, Any]] = []
    for epsilon_label, epsilon in zip(config["epsilon_ids"], config["epsilons"]):
        for tier in ("primary24",):
            seeds = config["seeds"]
            vectors = [
                lookup[(tier, epsilon_label, seed)]
                for seed in seeds
                if (tier, epsilon_label, seed) in lookup
            ]
            coefficients: list[complex] = []
            residuals: list[np.ndarray] = []
            orthogonalities: list[float] = []
            for vector in vectors:
                coefficient, residual, orthogonality = project_vector(vector, shape)
                coefficients.append(coefficient)
                residuals.append(residual)
                orthogonalities.append(orthogonality)
            component_rows = []
            nonlocal_rows = []
            for index, cosine in enumerate(config["physical_cosines"]):
                component_values = [complex(vector[index]) for vector in vectors]
                nonlocal_values = [complex(vector[index]) for vector in residuals]
                component_rows.append(
                    {
                        "physical_s_channel_cosine": cosine,
                        "estimate": (
                            aggregate_complex(component_values)
                            if component_values
                            else None
                        ),
                    }
                )
                nonlocal_rows.append(
                    {
                        "physical_s_channel_cosine": cosine,
                        "estimate": (
                            aggregate_complex(nonlocal_values)
                            if nonlocal_values
                            else None
                        ),
                    }
                )
            rows.append(
                {
                    "epsilon_id": epsilon_label,
                    "epsilon": epsilon,
                    "tier": tier,
                    "complete_scrambles": len(vectors),
                    "expected_scrambles": len(seeds),
                    "cyclic_components": component_rows,
                    "local_coefficient": (
                        aggregate_complex(coefficients) if coefficients else None
                    ),
                    "nonlocal_components": nonlocal_rows,
                    "maximum_eventwise_projection_orthogonality_residual": (
                        max(orthogonalities) if orthogonalities else None
                    ),
                }
            )
    return rows


def paired_convergence(
    config: dict[str, Any],
    lookup: dict[tuple[str, str, int], np.ndarray],
) -> list[dict[str, Any]]:
    shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
    rows: list[dict[str, Any]] = []
    for from_label, to_label, from_epsilon, to_epsilon in zip(
        config["epsilon_ids"],
        config["epsilon_ids"][1:],
        config["epsilons"],
        config["epsilons"][1:],
    ):
        vector_differences: list[np.ndarray] = []
        local_differences: list[complex] = []
        nonlocal_differences: list[np.ndarray] = []
        for seed in config["seeds"]:
            from_key = ("primary24", from_label, seed)
            to_key = ("primary24", to_label, seed)
            if from_key not in lookup or to_key not in lookup:
                continue
            from_vector = lookup[from_key]
            to_vector = lookup[to_key]
            from_local, from_nonlocal, _ = project_vector(from_vector, shape)
            to_local, to_nonlocal, _ = project_vector(to_vector, shape)
            vector_differences.append(to_vector - from_vector)
            local_differences.append(to_local - from_local)
            nonlocal_differences.append(to_nonlocal - from_nonlocal)
        vector_component_rows = []
        nonlocal_component_rows = []
        for index, cosine in enumerate(config["physical_cosines"]):
            vector_values = [complex(value[index]) for value in vector_differences]
            nonlocal_values = [complex(value[index]) for value in nonlocal_differences]
            vector_component_rows.append(
                {
                    "physical_s_channel_cosine": cosine,
                    "estimate": aggregate_complex(vector_values) if vector_values else None,
                }
            )
            nonlocal_component_rows.append(
                {
                    "physical_s_channel_cosine": cosine,
                    "estimate": aggregate_complex(nonlocal_values) if nonlocal_values else None,
                }
            )
        mean_vector_difference = (
            np.mean(np.stack(vector_differences), axis=0)
            if vector_differences
            else None
        )
        mean_nonlocal_difference = (
            np.mean(np.stack(nonlocal_differences), axis=0)
            if nonlocal_differences
            else None
        )
        local_estimate = (
            aggregate_complex(local_differences) if local_differences else None
        )
        rows.append(
            {
                "from_epsilon_id": from_label,
                "to_epsilon_id": to_label,
                "from_epsilon": from_epsilon,
                "to_epsilon": to_epsilon,
                "paired_scrambles": len(vector_differences),
                "expected_scrambles": len(config["seeds"]),
                "cyclic_component_differences": vector_component_rows,
                "full_vector_mean_step_L2": (
                    float(np.linalg.norm(mean_vector_difference))
                    if mean_vector_difference is not None
                    else None
                ),
                "local_coefficient_difference": local_estimate,
                "local_coefficient_mean_step_magnitude": (
                    abs(complex_from_row(local_estimate["mean"]))
                    if local_estimate is not None
                    else None
                ),
                "nonlocal_component_differences": nonlocal_component_rows,
                "nonlocal_mean_step_magnitudes": (
                    [float(abs(value)) for value in mean_nonlocal_difference]
                    if mean_nonlocal_difference is not None
                    else None
                ),
            }
        )
    return rows


def convergence_diagnostics(paired: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "effective_order_defined": False,
        "linear_epsilon_model_tested_not_assumed": True,
    }
    if len(paired) < 2:
        return result
    first, second = paired[0], paired[1]
    full_first = first["full_vector_mean_step_L2"]
    full_second = second["full_vector_mean_step_L2"]
    local_first = first["local_coefficient_mean_step_magnitude"]
    local_second = second["local_coefficient_mean_step_magnitude"]
    nonlocal_first = first["nonlocal_mean_step_magnitudes"]
    nonlocal_second = second["nonlocal_mean_step_magnitudes"]
    if all(value is not None and value > 0.0 for value in (full_first, full_second)):
        result.update(
            {
                "effective_order_defined": True,
                "full_vector_effective_order": math.log(full_first / full_second, 2.0),
                "full_vector_step_contracts": full_second < full_first,
                "full_vector_first_step_L2": full_first,
                "full_vector_second_step_L2": full_second,
            }
        )
    if all(value is not None and value > 0.0 for value in (local_first, local_second)):
        result.update(
            {
                "local_coefficient_effective_order": math.log(
                    local_first / local_second, 2.0
                ),
                "local_coefficient_step_contracts": local_second < local_first,
                "local_coefficient_first_step": local_first,
                "local_coefficient_second_step": local_second,
            }
        )
    if nonlocal_first is not None and nonlocal_second is not None:
        component_rows = []
        for index, (first_value, second_value) in enumerate(
            zip(nonlocal_first, nonlocal_second)
        ):
            component_rows.append(
                {
                    "component_index": index,
                    "first_step": first_value,
                    "second_step": second_value,
                    "contracts": second_value < first_value,
                    "effective_order": (
                        math.log(first_value / second_value, 2.0)
                        if first_value > 0.0 and second_value > 0.0
                        else None
                    ),
                }
            )
        result["nonlocal_component_diagnostics"] = component_rows
        result["all_nonlocal_component_steps_contract"] = all(
            row["contracts"] for row in component_rows
        )
    return result


def epsilon_zero_diagnostic(
    config: dict[str, Any],
    lookup: dict[tuple[str, str, int], np.ndarray],
) -> dict[str, Any]:
    if len(config["epsilon_ids"]) < 2:
        return {"available": False, "target_fitted": False}
    larger_label = config["epsilon_ids"][-2]
    smaller_label = config["epsilon_ids"][-1]
    ratio = config["epsilons"][-2] / config["epsilons"][-1]
    if abs(ratio - 2.0) > 1.0e-12:
        return {"available": False, "target_fitted": False}
    shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
    extrapolated: list[np.ndarray] = []
    local_coefficients: list[complex] = []
    nonlocal_vectors: list[np.ndarray] = []
    orthogonalities: list[float] = []
    for seed in config["seeds"]:
        larger_key = ("primary24", larger_label, seed)
        smaller_key = ("primary24", smaller_label, seed)
        if larger_key not in lookup or smaller_key not in lookup:
            continue
        vector = 2.0 * lookup[smaller_key] - lookup[larger_key]
        coefficient, residual, orthogonality = project_vector(vector, shape)
        extrapolated.append(vector)
        local_coefficients.append(coefficient)
        nonlocal_vectors.append(residual)
        orthogonalities.append(orthogonality)
    component_rows = []
    nonlocal_rows = []
    target = {
        canonical_float(row["physical_s_channel_cosine"]): row
        for row in config["target_rows"]
    }
    target_comparison = []
    for index, cosine in enumerate(config["physical_cosines"]):
        component_values = [complex(vector[index]) for vector in extrapolated]
        nonlocal_values = [complex(vector[index]) for vector in nonlocal_vectors]
        component_estimate = aggregate_complex(component_values) if component_values else None
        nonlocal_estimate = aggregate_complex(nonlocal_values) if nonlocal_values else None
        component_rows.append(
            {
                "physical_s_channel_cosine": cosine,
                "estimate": component_estimate,
            }
        )
        nonlocal_rows.append(
            {
                "physical_s_channel_cosine": cosine,
                "estimate": nonlocal_estimate,
            }
        )
        if nonlocal_estimate is not None:
            target_value = target[canonical_float(cosine)][
                "required_matched_hhh_nonlocal_cyclic_D_over_G3"
            ]
            predicted = float(nonlocal_estimate["mean"]["real"])
            target_comparison.append(
                {
                    "physical_s_channel_cosine": cosine,
                    "predicted_extrapolated_nonlocal_real": predicted,
                    "RQMC_standard_error": nonlocal_estimate[
                        "real_standard_error"
                    ],
                    "fixed_5018_target": target_value,
                    "predicted_minus_target": predicted - target_value,
                }
            )
    rms = (
        float(
            np.sqrt(
                np.mean(
                    [row["predicted_minus_target"] ** 2 for row in target_comparison]
                )
            )
        )
        if target_comparison
        else None
    )
    return {
        "available": len(extrapolated) == len(config["seeds"]),
        "model": "linear Richardson diagnostic 2*C(0.02)-C(0.04)",
        "paired_scrambles": len(extrapolated),
        "cyclic_components": component_rows,
        "local_coefficient": (
            aggregate_complex(local_coefficients) if local_coefficients else None
        ),
        "nonlocal_components": nonlocal_rows,
        "maximum_eventwise_projection_orthogonality_residual": (
            max(orthogonalities) if orthogonalities else None
        ),
        "fixed_5018_target_comparison": target_comparison,
        "RMS_nonlocal_target_difference": rms,
        "target_loaded_after_decomposition": True,
        "target_fitted": False,
        "epsilon_zero_claimed": False,
        "valid_for_full_MTS_claim": False,
    }


def global_tier_audit(
    config: dict[str, Any],
    jobs: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    central = min(
        config["crossings"],
        key=lambda row: abs(row["physical_s_channel_cosine"]),
    )
    direct: dict[tuple[str, str, int, int, str], complex] = {}
    for job in jobs.values():
        if numeric_job(job):
            direct[
                (
                    job["tier"],
                    job["epsilon_id"],
                    int(job["seed"]),
                    int(job["sample_index"]),
                    job["base_argument_id"],
                )
            ] = complex_from_row(job["normalized_direct_D_hhh_over_G3"])
    rows = []
    for epsilon_label, epsilon in zip(config["epsilon_ids"], config["epsilons"]):
        values: dict[str, complex] = {}
        for tier in ("primary24", "audit32"):
            sample_values: list[complex] = []
            for sample_index in range(config["samples_per_seed"]):
                keys = [
                    (
                        tier,
                        epsilon_label,
                        config["audit_seed"],
                        sample_index,
                        central[name],
                    )
                    for name in (
                        "s_argument_id",
                        "t_argument_id",
                        "u_argument_id",
                    )
                ]
                if all(key in direct for key in keys):
                    sample_values.append(
                        direct[keys[0]]
                        + central["t_ratio"] ** 3 * direct[keys[1]]
                        + central["u_ratio"] ** 3 * direct[keys[2]]
                    )
            if len(sample_values) == config["samples_per_seed"]:
                values[tier] = complex(np.mean(sample_values))
        if "primary24" not in values or "audit32" not in values:
            rows.append({"epsilon": epsilon, "complete": False})
            continue
        primary = values["primary24"]
        audit = values["audit32"]
        difference = audit - primary
        rows.append(
            {
                "epsilon": epsilon,
                "complete": True,
                "primary24": complex_row(primary),
                "audit32": complex_row(audit),
                "difference": complex_row(difference),
                "relative_difference": abs(difference)
                / max(abs(audit), 1.0),
            }
        )
    return rows


def build_summary(
    config: dict[str, Any], jobs: dict[str, dict[str, Any]], run_state: str
) -> dict[str, Any]:
    expected = expected_jobs(config)
    expected_keys = {row["job_key"] for row in expected}
    terminal_keys = set(jobs) & expected_keys
    per_seed, lookup = cyclic_seed_vectors(config, jobs)
    summaries = vector_summaries(config, lookup)
    paired = paired_convergence(config, lookup)
    diagnostics = convergence_diagnostics(paired)
    extrapolation = epsilon_zero_diagnostic(config, lookup)
    audit = global_tier_audit(config, jobs)
    all_numeric = len(terminal_keys) == len(expected_keys) and all(
        numeric_job(jobs[key]) for key in expected_keys
    )
    primary_complete = all(
        row["complete_scrambles"] == row["expected_scrambles"]
        for row in summaries
        if row["tier"] == "primary24"
    )
    audit_complete = all(row.get("complete", False) for row in audit)
    audit_consistent = audit_complete and all(
        row["relative_difference"]
        <= config["numerical_gate_thresholds"][
            "maximum_global_tier_relative_difference"
        ]
        for row in audit
    )
    orthogonalities = [
        row["maximum_eventwise_projection_orthogonality_residual"]
        for row in summaries
        if row["maximum_eventwise_projection_orthogonality_residual"] is not None
    ]
    projection_exact = bool(orthogonalities) and max(orthogonalities) <= config[
        "numerical_gate_thresholds"
    ]["maximum_projection_orthogonality_residual"]
    full_contracts = bool(diagnostics.get("full_vector_step_contracts", False))
    local_contracts = bool(
        diagnostics.get("local_coefficient_step_contracts", False)
    )
    nonlocal_contracts = bool(
        diagnostics.get("all_nonlocal_component_steps_contract", False)
    )
    stable = (
        all_numeric
        and primary_complete
        and audit_consistent
        and projection_exact
        and full_contracts
        and local_contracts
        and nonlocal_contracts
    )
    gate = {
        "all_expected_jobs_numeric_and_converged": all_numeric,
        "all_three_primary_vectors_complete": primary_complete,
        "global24_global32_audit_complete": audit_complete,
        "global24_global32_within_threshold": audit_consistent,
        "eventwise_local_nonlocal_projection_orthogonal": projection_exact,
        "full_vector_mean_step_contracts": full_contracts,
        "local_coefficient_mean_step_contracts": local_contracts,
        "all_five_nonlocal_mean_steps_contract": nonlocal_contracts,
        "paired_full_vector_ladder_stable": stable,
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
            jobs[key].get("status") == "IMPORTED_CONVERGED" for key in terminal_keys
        ),
        "computed_converged_jobs": sum(
            jobs[key].get("status") == "COMPLETED_CONVERGED" for key in terminal_keys
        ),
        "failed_jobs": sum(
            jobs[key].get("status") == "FAILED" for key in terminal_keys
        ),
        "unconverged_jobs": sum(
            jobs[key].get("status") == "COMPLETED_UNCONVERGED"
            for key in terminal_keys
        ),
        "cyclic_vectors_per_seed": per_seed,
        "vector_summaries": summaries,
        "paired_convergence": paired,
        "convergence_diagnostics": diagnostics,
        "linear_epsilon_zero_diagnostic": extrapolation,
        "global_tier_audit": audit,
        "gate": gate,
        "target_fitted": False,
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
    vector_rows: list[dict[str, Any]] = []
    decomposition_rows: list[dict[str, Any]] = []
    for vector_summary in summary["vector_summaries"]:
        for component, nonlocal_component in zip(
            vector_summary["cyclic_components"],
            vector_summary["nonlocal_components"],
        ):
            estimate = component["estimate"]
            nonlocal_estimate = nonlocal_component["estimate"]
            vector_rows.append(
                {
                    "epsilon": vector_summary["epsilon"],
                    "tier": vector_summary["tier"],
                    "physical_s_channel_cosine": component[
                        "physical_s_channel_cosine"
                    ],
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
                    "scrambles": (
                        estimate["replicate_count"] if estimate else 0
                    ),
                }
            )
            local = vector_summary["local_coefficient"]
            decomposition_rows.append(
                {
                    "epsilon": vector_summary["epsilon"],
                    "tier": vector_summary["tier"],
                    "physical_s_channel_cosine": component[
                        "physical_s_channel_cosine"
                    ],
                    "local_coefficient_mean_real": (
                        local["mean"]["real"] if local else ""
                    ),
                    "local_coefficient_mean_imaginary": (
                        local["mean"]["imaginary"] if local else ""
                    ),
                    "nonlocal_mean_real": (
                        nonlocal_estimate["mean"]["real"]
                        if nonlocal_estimate
                        else ""
                    ),
                    "nonlocal_mean_imaginary": (
                        nonlocal_estimate["mean"]["imaginary"]
                        if nonlocal_estimate
                        else ""
                    ),
                    "nonlocal_real_standard_error": (
                        nonlocal_estimate["real_standard_error"]
                        if nonlocal_estimate
                        else ""
                    ),
                }
            )
    write_csv(
        VECTOR_CSV,
        vector_rows,
        [
            "epsilon",
            "tier",
            "physical_s_channel_cosine",
            "mean_real",
            "mean_imaginary",
            "real_standard_error",
            "imaginary_standard_error",
            "scrambles",
        ],
    )
    write_csv(
        DECOMPOSITION_CSV,
        decomposition_rows,
        [
            "epsilon",
            "tier",
            "physical_s_channel_cosine",
            "local_coefficient_mean_real",
            "local_coefficient_mean_imaginary",
            "nonlocal_mean_real",
            "nonlocal_mean_imaginary",
            "nonlocal_real_standard_error",
        ],
    )
    paired_rows: list[dict[str, Any]] = []
    for step in summary["paired_convergence"]:
        paired_rows.append(
            {
                "from_epsilon": step["from_epsilon"],
                "to_epsilon": step["to_epsilon"],
                "paired_scrambles": step["paired_scrambles"],
                "full_vector_mean_step_L2": step["full_vector_mean_step_L2"],
                "local_coefficient_mean_step_magnitude": step[
                    "local_coefficient_mean_step_magnitude"
                ],
                "nonlocal_component_step_magnitudes": json.dumps(
                    step["nonlocal_mean_step_magnitudes"], separators=(",", ":")
                ),
            }
        )
    write_csv(
        PAIRED_CSV,
        paired_rows,
        [
            "from_epsilon",
            "to_epsilon",
            "paired_scrambles",
            "full_vector_mean_step_L2",
            "local_coefficient_mean_step_magnitude",
            "nonlocal_component_step_magnitudes",
        ],
    )
    target_rows = summary["linear_epsilon_zero_diagnostic"].get(
        "fixed_5018_target_comparison", []
    )
    write_csv(
        TARGET_CSV,
        target_rows,
        [
            "physical_s_channel_cosine",
            "predicted_extrapolated_nonlocal_real",
            "RQMC_standard_error",
            "fixed_5018_target",
            "predicted_minus_target",
        ],
    )
    write_csv(
        GATE_CSV,
        [
            {
                "check": key,
                "passed": value,
                "valid_for_full_MTS_claim": False,
            }
            for key, value in summary["gate"].items()
        ],
        ["check", "passed", "valid_for_full_MTS_claim"],
    )
    atomic_text(
        PROVENANCE,
        f"""# 5036 provenance

- Marker: `{MARKER}`.
- Run directory: `{run_directory}`.
- Config digest: `{config['config_digest']}`.
- Full `epsilon=0.08` source: `post-checkpoint-work/source-intake/functional_rg/5034/runs/bounded_smoke_eps008_v2`.
- Paired central source: `post-checkpoint-work/source-intake/functional_rg/5035/runs/central_eps008_004_002_s4_v1`.
- Shrinking-radius rule: `post-checkpoint-work/scripts/Y5_R2FR_5035_pair_local_residue_radius_repair.py`.
- Fixed comparison rows: `post-checkpoint-work/source-intake/functional_rg/5018/known_master_without_hhh_and_matched_hhh_target.csv`.
- Every import requires exact epsilon, event, argument and tier identity plus a source-job SHA-256 digest.
- Every new kernel uses its own canonical projective Feynman homotopy and the v4 shrinking-radius residue rule.
- Local/nonlocal projection is eventwise and precedes loading the fixed 5018 comparison values.
- Raised paths, representative kernels and target fitting are forbidden.
- This is a two-scramble convergence diagnostic, not production precision or a full-MTS claim.
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
            "base_argument_count": len(config["base_arguments"]),
            "physical_component_count": len(config["crossings"]),
            "expected_jobs": len(expected),
            "expected_primary_jobs": sum(
                row["tier"] == "primary24" for row in expected
            ),
            "expected_audit_jobs": sum(row["tier"] == "audit32" for row in expected),
            "target_fitted": False,
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
        f"invocation start terminal={len(jobs)} expected={len(expected)} imports={imported} max_wall={arguments.max_wall_seconds}",
    )
    new_kernels = 0
    state = "COMPLETE"
    N5030.chamber_residue_catalog = MREPAIR.repaired_chamber_residue_catalog
    try:
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
            result = execute_new_job(run_directory, config, job)
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
    finally:
        N5030.chamber_residue_catalog = ORIGINAL_CATALOG
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
    parser.add_argument("--run-id", default="paired_full_vector_s2_v1")
    parser.add_argument("--physical-cosines", default="-0.6,-0.3,0,0.3,0.6")
    parser.add_argument("--epsilons", default="0.08,0.04,0.02")
    parser.add_argument("--seeds", default="503401,503402")
    parser.add_argument("--power", type=int, default=0)
    parser.add_argument("--topology-steps", type=int, default=96)
    parser.add_argument("--topology-maximum-steps", type=int, default=49152)
    parser.add_argument("--regulator", type=float, default=1.0e-3)
    parser.add_argument("--boundary-tracking-steps", type=int, default=64)
    parser.add_argument("--max-wall-seconds", type=float, default=10800.0)
    parser.add_argument("--max-new-kernels", type=int)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_wall_seconds <= 0.0:
        raise ValueError("max wall seconds must be positive")
    result = run(arguments)
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
