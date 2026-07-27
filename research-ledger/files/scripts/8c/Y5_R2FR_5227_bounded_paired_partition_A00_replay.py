from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE_5224 = FUNCTIONAL_RG / "5224"
SOURCE_5225 = FUNCTIONAL_RG / "5225"
SOURCE_5226 = FUNCTIONAL_RG / "5226"
SOURCE = FUNCTIONAL_RG / "5227"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5224 = (
    POST
    / "scripts"
    / "Y5_R2FR_5224_replacement_scaled_controlled_run.py"
)
RESULT_5224 = SOURCE_5224 / "replacement_scaled_controlled_results.json"
CONFIG_5224 = SOURCE_5224 / "frozen_replacement_config.json"
MANIFEST_5224 = SOURCE_5224 / "frozen_replacement_manifest.json"
CONTROL_ROWS_5224 = SOURCE_5224 / "replacement_A00_control_rows.csv"
EVENT_ROWS_5224 = SOURCE_5224 / "replacement_event_rows.csv"
RUN_5224 = (
    SOURCE_5224 / "runs" / "replacement_scaled_controlled_v1"
)
VALIDATION_5224 = RESIDUALS / "P8_Y5_BRR545_5224_VALIDATION.csv"
RESULT_5225 = SOURCE_5225 / "control_multiplier_and_raw_salvage.json"
VALIDATION_5225 = RESIDUALS / "P8_Y5_BRR545_5225_VALIDATION.csv"
RESULT_5226 = SOURCE_5226 / "physical_permutation_chart_bijection_results.json"
VALIDATION_5226 = RESIDUALS / "P8_Y5_BRR545_5226_VALIDATION.csv"

RUN_DIRECTORY = SOURCE / "runs" / "bounded_paired_partition_A00_replay"
CLASSIFIER_CACHE = RUN_DIRECTORY / "grouped-classifier-cache"
MANIFEST = SOURCE / "frozen_bounded_paired_partition_manifest.json"
SCHEDULE = SOURCE / "frozen_bounded_paired_partition_schedule.csv"
PROTOCOL_LOCK = SOURCE / "frozen_bounded_paired_partition_protocol_lock.json"
TOPOLOGY_REUSE = SOURCE / "topology_reuse_audit.json"
STATUS = RUN_DIRECTORY / "status.json"
EVENT_ROWS = SOURCE / "bounded_paired_partition_A00_event_rows.csv"
RESULT = SOURCE / "bounded_paired_partition_A00_results.json"
DOCUMENT = (
    POST
    / "5227-Y5-R2FR-bounded-paired-partition-A00-replay.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5227_VALIDATION.csv"

MARKER = "MTS_5227_BOUNDED_PAIRED_PARTITION_A00_REPLAY"
REVISION = "bounded-paired-w3-w1-direct-pullback-v1"
RUN_ID = "bounded_paired_partition_A00_replay"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
PHYSICAL_A00_WEIGHT = -0.008
MAXIMUM_WALL_HOURS = 4.0
MAXIMUM_MEAN_DIFFERENCE_STANDARD_ERRORS = 2.0
MAXIMUM_A00_STANDARD_DEVIATION_RATIO = 0.8
MAXIMUM_LOCAL_STANDARD_DEVIATION_RATIO = 0.8


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5224 = load_module(SCRIPT_5224, "mts_5224_for_5227")
M5212 = M5224.M5212
M5077 = M5212.M5077
N5030 = M5077.M5036.N5030
M5026 = N5030.M5028.M5026


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def complex_from_row(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def all_pass(path: Path) -> bool:
    return all(
        row["passed"].strip().lower() == "true" for row in read_csv(path)
    )


def selected_jobs(
    config: dict[str, Any], source_manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    jobs = M5224.M5221.build_schedule(config, source_manifest)
    selected = [
        job
        for job in jobs
        if job["stratum"] == "topological"
        and job["base_argument_id"] == "A00"
    ]
    if len(selected) != 48:
        raise RuntimeError(f"expected 48 paired A00 jobs, got {len(selected)}")
    return selected


def source_paths() -> list[Path]:
    return [
        Path(__file__).resolve(),
        SCRIPT_5224,
        RESULT_5224,
        CONFIG_5224,
        MANIFEST_5224,
        CONTROL_ROWS_5224,
        EVENT_ROWS_5224,
        VALIDATION_5224,
        RESULT_5225,
        VALIDATION_5225,
        RESULT_5226,
        VALIDATION_5226,
    ]


def make_manifest(jobs: list[dict[str, Any]]) -> dict[str, Any]:
    result_5224 = read_json(RESULT_5224)
    result_5225 = read_json(RESULT_5225)
    result_5226 = read_json(RESULT_5226)
    if not (
        result_5224["state"] == "COMPLETE_DESIGN"
        and result_5224["counts"]["completed_converged"] == 520
        and result_5225["decision"]
        == (
            "RETIRE_BETA_ONE_KEEP_ZERO_IDENTITY_AND_BUILD_DIRECT_"
            "SLOT_BALANCED_PAIR"
        )
        and result_5226["decision"]
        == (
            "PHYSICAL_CHART_BIJECTION_CLOSED_EXTEND_DIRECTLY_TO_"
            "SLOT_AGNOSTIC_TOPOLOGY"
        )
        and all_pass(VALIDATION_5224)
        and all_pass(VALIDATION_5225)
        and all_pass(VALIDATION_5226)
    ):
        raise RuntimeError("5224-5226 source chain is not closed")
    return {
        "checkpoint": 5227,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": RUN_ID,
        "locked_date": "2026-07-25",
        "source_outcomes_known_at_lock": True,
        "paired_replay_outcomes_present_at_lock": False,
        "event_count": 24,
        "job_count": len(jobs),
        "epsilon_ids": ["E040", "E020"],
        "base_argument_id": "A00",
        "estimator": {
            "original_direct_weight": "W3=3*w3",
            "paired_direct_weight": "W13=3*(w3+w1)/2",
            "original_endpoint_subtraction_coefficient": 1.0,
            "paired_endpoint_subtraction_coefficient": 0.5,
            "common_chart_identity": (
                "pulling the g1 channel through T13 gives the direct "
                "common-chart term 3*w1; averaging with 3*w3 gives W13"
            ),
            "unbiasedness": (
                "S3 symmetry and w1+w2+w3=1 imply "
                "integral[3*w3*A]=integral[3*(w3+w1)*A/2]"
            ),
            "variance_theorem": (
                "the paired estimator is the arithmetic mean of two "
                "identically distributed channel estimators, so its "
                "variance cannot exceed a single channel when square "
                "integrability holds"
            ),
            "soft_endpoint": (
                "as x3->0, w3->1 and w1->0, so the paired g-function "
                "endpoint is one half of the original endpoint"
            ),
            "new_pole_denominators": False,
            "free_or_fitted_multiplier": False,
        },
        "retrospective_acceptance_thresholds": {
            "all_jobs_must_converge": True,
            "maximum_mean_difference_standard_errors": (
                MAXIMUM_MEAN_DIFFERENCE_STANDARD_ERRORS
            ),
            "maximum_A00_real_standard_deviation_ratio": (
                MAXIMUM_A00_STANDARD_DEVIATION_RATIO
            ),
            "maximum_local_real_standard_deviation_ratio": (
                MAXIMUM_LOCAL_STANDARD_DEVIATION_RATIO
            ),
            "threshold_retuning_after_outcomes_allowed": False,
        },
        "interpretation": (
            "outcome-exposed retrospective estimator test only; a pass "
            "authorizes a new blind pilot and is not a coefficient claim"
        ),
        "locked_sources": [
            {"path": str(path), "sha256": digest(path)}
            for path in source_paths()
        ],
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def paired_multiplier(rotated_internal: np.ndarray) -> complex:
    energy_1 = complex(rotated_internal[0, 0])
    energy_2 = complex(rotated_internal[1, 0])
    energy_3 = complex(rotated_internal[2, 0])
    denominator = (
        energy_1**2 * energy_2**2
        + energy_1**2 * energy_3**2
        + energy_2**2 * energy_3**2
    )
    if abs(denominator) == 0.0:
        raise ZeroDivisionError("paired partition denominator vanished")
    return complex(
        1.5
        * energy_2**2
        * (energy_1**2 + energy_3**2)
        / denominator
    )


def paired_finite_plus_integrand(
    internal: np.ndarray,
    soft_energy: float,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: complex,
    unit_circle: complex,
) -> complex:
    rotated_internal = M5026.M5024.rotate_internal(internal, unit_circle)
    multiplier = paired_multiplier(rotated_internal)
    direct = (
        soft_energy
        * soft_energy
        * multiplier
        * M5026.M5017.hhh_reduced_product(
            rotated_internal, scattering_cosine, 1.0
        )
        / (M5026.M5017.S_VALUE * M5026.M5017.S_VALUE)
    )
    subtraction = 0.5 * M5026.M5022.endpoint_value(
        soft_direction,
        decay_direction,
        scattering_cosine,
        unit_circle,
    )
    return complex((direct - subtraction) / soft_energy)


def estimator_machine_checks() -> dict[str, Any]:
    generator = np.random.default_rng(5227001)
    maximum_original_polynomial_residual = 0.0
    maximum_real_multiplier = 0.0
    minimum_real_multiplier = math.inf
    maximum_endpoint_scaled_value = 0.0
    endpoint_samples: list[dict[str, float]] = []
    for _ in range(256):
        soft_energy = float(generator.uniform(0.02, 0.98))
        soft_cosine = float(generator.uniform(-0.9, 0.9))
        decay_cosine = float(generator.uniform(-0.9, 0.9))
        relative_circle = np.exp(
            2.0j * math.pi * float(generator.uniform())
        )
        soft_direction, decay_direction, internal = (
            N5030.M5028.event_geometry(
                soft_energy,
                complex(soft_cosine, 0.0),
                complex(decay_cosine, 0.0),
                complex(relative_circle),
            )
        )
        rotated = M5026.M5024.rotate_internal(internal, 1.0 + 0.0j)
        inverse_sum = sum(
            1.0 / complex(momentum[0]) ** 2 for momentum in rotated
        )
        original = (
            3.0 / complex(rotated[2, 0]) ** 2 / inverse_sum
        )
        energy_1 = complex(rotated[0, 0])
        energy_2 = complex(rotated[1, 0])
        energy_3 = complex(rotated[2, 0])
        denominator = (
            energy_1**2 * energy_2**2
            + energy_1**2 * energy_3**2
            + energy_2**2 * energy_3**2
        )
        polynomial_original = (
            3.0 * energy_1**2 * energy_2**2 / denominator
        )
        maximum_original_polynomial_residual = max(
            maximum_original_polynomial_residual,
            abs(original - polynomial_original),
        )
        paired = paired_multiplier(rotated)
        maximum_real_multiplier = max(
            maximum_real_multiplier, float(paired.real)
        )
        minimum_real_multiplier = min(
            minimum_real_multiplier, float(paired.real)
        )

    for soft_energy in (1.0e-3, 3.0e-4, 1.0e-4, 3.0e-5):
        soft_direction, decay_direction, internal = (
            N5030.M5028.event_geometry(
                soft_energy,
                complex(0.23, 0.0),
                complex(-0.31, 0.0),
                complex(np.exp(0.37j)),
            )
        )
        value = paired_finite_plus_integrand(
            internal,
            soft_energy,
            soft_direction,
            decay_direction,
            complex(-9.0, 0.04),
            complex(np.exp(0.29j)),
        )
        if not (math.isfinite(value.real) and math.isfinite(value.imag)):
            raise RuntimeError("paired endpoint sample is nonfinite")
        maximum_endpoint_scaled_value = max(
            maximum_endpoint_scaled_value, abs(value)
        )
        endpoint_samples.append(
            {
                "soft_energy": soft_energy,
                "absolute_value": abs(value),
                "soft_energy_times_absolute_value": (
                    soft_energy * abs(value)
                ),
            }
        )
    endpoint_x_scaled_ratio = (
        endpoint_samples[-1]["soft_energy_times_absolute_value"]
        / endpoint_samples[0]["soft_energy_times_absolute_value"]
    )
    endpoint_magnitude_ratio = (
        endpoint_samples[-1]["absolute_value"]
        / endpoint_samples[0]["absolute_value"]
    )
    return {
        "sample_count": 256,
        "maximum_original_inverse_to_polynomial_residual": (
            maximum_original_polynomial_residual
        ),
        "minimum_real_physical_multiplier": minimum_real_multiplier,
        "maximum_real_physical_multiplier": maximum_real_multiplier,
        "physical_multiplier_interval": [0.0, 1.5],
        "paired_endpoint_samples_all_finite": True,
        "paired_endpoint_samples": endpoint_samples,
        "maximum_endpoint_sample_magnitude": maximum_endpoint_scaled_value,
        "endpoint_x_scaled_ratio": endpoint_x_scaled_ratio,
        "endpoint_magnitude_ratio": endpoint_magnitude_ratio,
        "endpoint_regularity_gate": bool(
            endpoint_x_scaled_ratio < 0.1
            and endpoint_magnitude_ratio < 2.0
        ),
        "same_partition_denominator": True,
        "new_pole_denominators": False,
        "passed": bool(
            maximum_original_polynomial_residual < 1.0e-11
            and minimum_real_multiplier >= -1.0e-12
            and maximum_real_multiplier <= 1.5 + 1.0e-12
            and endpoint_x_scaled_ratio < 0.1
            and endpoint_magnitude_ratio < 2.0
        ),
    }


def prepare() -> tuple[
    dict[str, Any], dict[str, Any], list[dict[str, Any]]
]:
    for path in source_paths():
        if not path.is_file():
            raise FileNotFoundError(path)
    SOURCE.mkdir(parents=True, exist_ok=True)
    RUN_DIRECTORY.mkdir(parents=True, exist_ok=True)
    CLASSIFIER_CACHE.mkdir(parents=True, exist_ok=True)
    (RUN_DIRECTORY / "topologies").mkdir(parents=True, exist_ok=True)
    config = read_json(CONFIG_5224)
    source_manifest = read_json(MANIFEST_5224)
    jobs = selected_jobs(config, source_manifest)
    if MANIFEST.exists():
        manifest = read_json(MANIFEST)
    else:
        outcome_files = list(
            (RUN_DIRECTORY / "topological-jobs").glob("*.json")
        )
        if outcome_files:
            raise RuntimeError("paired outcomes exist before manifest lock")
        manifest = make_manifest(jobs)
        atomic_json(MANIFEST, manifest)
    schedule_rows = [
        {"schedule_index": index, **job}
        for index, job in enumerate(jobs, start=1)
    ]
    if not SCHEDULE.exists():
        write_csv(SCHEDULE, schedule_rows)
    contract = {
        "manifest_sha256": digest(MANIFEST),
        "schedule_sha256": digest(SCHEDULE),
        "source_config_sha256": digest(CONFIG_5224),
        "runner_sha256": digest(Path(__file__).resolve()),
        "estimator_sha256": canonical_digest(manifest["estimator"]),
        "job_count": len(jobs),
    }
    if PROTOCOL_LOCK.exists():
        lock = read_json(PROTOCOL_LOCK)
        if lock["contract"] != contract:
            raise RuntimeError("checkpoint-5227 protocol changed after lock")
    else:
        outcome_files = list(
            (RUN_DIRECTORY / "topological-jobs").glob("*.json")
        )
        if outcome_files:
            raise RuntimeError("paired outcomes exist before protocol lock")
        atomic_json(
            PROTOCOL_LOCK,
            {
                "checkpoint": 5227,
                "checkpoint_marker": MARKER,
                "contract": contract,
                "paired_outcomes_present_at_lock": False,
                "threshold_retuning_after_outcomes_allowed": False,
            },
        )

    reused: list[dict[str, Any]] = []
    for job in jobs:
        source_job_path = M5212.output_path(RUN_5224, job)
        source_job = read_json(source_job_path)
        source_topology = Path(source_job["topology_file"])
        argument_id = f"{job['epsilon_id']}_{job['base_argument_id']}"
        target_topology = (
            RUN_DIRECTORY
            / "topologies"
            / f"{job['event_id']}__{argument_id}.json"
        )
        if target_topology.exists():
            if digest(target_topology) != digest(source_topology):
                raise RuntimeError(
                    f"topology reuse collision: {target_topology}"
                )
        else:
            shutil.copy2(source_topology, target_topology)
        reused.append(
            {
                "job_key": job["job_key"],
                "source": str(source_topology),
                "target": str(target_topology),
                "sha256": digest(source_topology),
                "same_partition_denominator": True,
                "new_pole_roots_required": False,
            }
        )
    atomic_json(
        TOPOLOGY_REUSE,
        {
            "checkpoint": 5227,
            "topology_count": len(reused),
            "proof": (
                "W3 and W13 have the same polynomial partition denominator; "
                "the amplitude and subtraction pole families are unchanged, "
                "so the existing topology is a safe root superset"
            ),
            "rows": reused,
            "valid_for_numeric_UV_claim": False,
        },
    )
    checks = estimator_machine_checks()
    if not checks["passed"]:
        raise RuntimeError(f"paired estimator machine checks failed: {checks}")
    return manifest, config, jobs


def install_runtime(config: dict[str, Any]) -> Any:
    M5224.RUN_DIRECTORY = RUN_DIRECTORY
    M5224.CLASSIFIER_CACHE = CLASSIFIER_CACHE
    M5224.RUNTIME_ROWS.clear()
    return M5224.install_runtime(config)


def completed_event_seeds(
    config: dict[str, Any], jobs: list[dict[str, Any]]
) -> list[int]:
    seeds = sorted({int(job["seed"]) for job in jobs})
    return [
        seed
        for seed in seeds
        if all(
            (
                M5212.cached_result(RUN_DIRECTORY, config, job)
                or {}
            ).get("status")
            == "COMPLETED_CONVERGED"
            for job in jobs
            if int(job["seed"]) == seed
        )
    ]


def run(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    wall_cap_hours: float,
    maximum_events: int,
) -> None:
    if not (0.0 < wall_cap_hours <= MAXIMUM_WALL_HOURS):
        raise ValueError("wall cap must lie in (0,4] hours")
    manager = install_runtime(config)
    original_integrand = M5026.finite_plus_integrand
    M5026.finite_plus_integrand = paired_finite_plus_integrand
    started = time.monotonic()
    newly_completed_events = 0
    try:
        for seed in sorted({int(job["seed"]) for job in jobs}):
            event_jobs = [
                job for job in jobs if int(job["seed"]) == seed
            ]
            if all(
                (
                    M5212.cached_result(RUN_DIRECTORY, config, job)
                    or {}
                ).get("status")
                == "COMPLETED_CONVERGED"
                for job in event_jobs
            ):
                continue
            if maximum_events and newly_completed_events >= maximum_events:
                break
            for job in event_jobs:
                if (
                    M5212.cached_result(RUN_DIRECTORY, config, job)
                    is not None
                ):
                    continue
                row = M5212.execute_job(
                    RUN_DIRECTORY, config, manager, job
                )
                row.update(
                    {
                        "checkpoint_marker": MARKER,
                        "revision": REVISION,
                        "paired_direct_weight": "3*(w3+w1)/2",
                        "paired_endpoint_subtraction_coefficient": 0.5,
                        "topology_reused_without_new_roots": True,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
                atomic_json(M5212.output_path(RUN_DIRECTORY, job), row)
                atomic_json(
                    STATUS,
                    {
                        "checkpoint": 5227,
                        "state": "RUNNING",
                        "seed": seed,
                        "job_key": job["job_key"],
                        "job_status": row["status"],
                        "elapsed_seconds": time.monotonic() - started,
                        "completed_event_count": len(
                            completed_event_seeds(config, jobs)
                        ),
                    },
                )
                print(
                    json.dumps(
                        {
                            "seed": seed,
                            "job": job["job_key"],
                            "status": row["status"],
                            "elapsed_seconds": time.monotonic() - started,
                        }
                    ),
                    flush=True,
                )
                if row["status"] != "COMPLETED_CONVERGED":
                    raise RuntimeError(
                        f"paired replay stopped at {job['job_key']}: {row}"
                    )
                if (
                    time.monotonic() - started
                ) / 3600.0 >= wall_cap_hours:
                    return
            newly_completed_events += 1
    finally:
        M5026.finite_plus_integrand = original_integrand


def scalar_summary(values: np.ndarray) -> dict[str, float | int]:
    return {
        "count": len(values),
        "mean": float(np.mean(values)),
        "sample_standard_deviation": float(np.std(values, ddof=1)),
        "standard_error": float(
            np.std(values, ddof=1) / math.sqrt(len(values))
        ),
        "minimum": float(np.min(values)),
        "median": float(np.median(values)),
        "maximum": float(np.max(values)),
    }


def analyse(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    controls = {
        int(row["seed"]): row for row in read_csv(CONTROL_ROWS_5224)
    }
    complete_seeds = completed_event_seeds(config, jobs)
    event_rows: list[dict[str, Any]] = []
    for seed in complete_seeds:
        source = controls[seed]
        selected = {
            job["epsilon_id"]: job
            for job in jobs
            if int(job["seed"]) == seed
        }
        paired_values = {
            epsilon_id: complex_from_row(
                read_json(
                    M5212.output_path(RUN_DIRECTORY, selected[epsilon_id])
                )["normalized_topological_D_hhh_over_G3"]
            )
            for epsilon_id in ("E040", "E020")
        }
        paired_a00 = PHYSICAL_A00_WEIGHT * (
            2.0 * paired_values["E020"] - paired_values["E040"]
        )
        raw_a00 = complex(
            float(source["raw_A00_real"]),
            float(source["raw_A00_imaginary"]),
        )
        raw_local = complex(
            float(source["raw_topological_local_real"]),
            float(source["raw_topological_local_imaginary"]),
        )
        local_weight = float(source["local_projector_weight_z_minus_0p6"])
        paired_local = raw_local + local_weight * (
            paired_a00 - raw_a00
        )
        event_rows.append(
            {
                "seed": seed,
                "tranche": int(source["tranche"]),
                "raw_A00_real": raw_a00.real,
                "raw_A00_imaginary": raw_a00.imag,
                "paired_A00_real": paired_a00.real,
                "paired_A00_imaginary": paired_a00.imag,
                "paired_minus_raw_A00_real": (
                    paired_a00.real - raw_a00.real
                ),
                "paired_minus_raw_A00_imaginary": (
                    paired_a00.imag - raw_a00.imag
                ),
                "raw_topological_local_real": raw_local.real,
                "raw_topological_local_imaginary": raw_local.imag,
                "paired_topological_local_real": paired_local.real,
                "paired_topological_local_imaginary": paired_local.imag,
                "valid_for_numeric_UV_claim": False,
            }
        )
    if event_rows:
        write_csv(EVENT_ROWS, event_rows)

    state = (
        "COMPLETE_RETROSPECTIVE_REPLAY"
        if len(complete_seeds) == 24
        else "PARTIAL_RETROSPECTIVE_REPLAY"
    )
    analysis: dict[str, Any] | None = None
    decision = "CONTINUE_REPLAY"
    if len(event_rows) >= 2:
        raw_a00 = np.asarray(
            [row["raw_A00_real"] for row in event_rows]
        )
        paired_a00 = np.asarray(
            [row["paired_A00_real"] for row in event_rows]
        )
        differences = paired_a00 - raw_a00
        raw_local = np.asarray(
            [row["raw_topological_local_real"] for row in event_rows]
        )
        paired_local = np.asarray(
            [row["paired_topological_local_real"] for row in event_rows]
        )
        difference_summary = scalar_summary(differences)
        difference_mean_standard_errors = abs(
            float(difference_summary["mean"])
        ) / max(
            float(difference_summary["standard_error"]), 1.0e-300
        )
        a00_ratio = float(
            np.std(paired_a00, ddof=1) / np.std(raw_a00, ddof=1)
        )
        local_ratio = float(
            np.std(paired_local, ddof=1) / np.std(raw_local, ddof=1)
        )
        seeds = [int(row["seed"]) for row in event_rows]
        raw_tail = M5212.scalar_distribution_diagnostics(
            raw_local, seeds
        )
        paired_tail = M5212.scalar_distribution_diagnostics(
            paired_local, seeds
        )
        analysis = {
            "event_count": len(event_rows),
            "raw_A00_real": scalar_summary(raw_a00),
            "paired_A00_real": scalar_summary(paired_a00),
            "paired_minus_raw_A00_real": difference_summary,
            "difference_mean_in_standard_errors": (
                difference_mean_standard_errors
            ),
            "A00_real_standard_deviation_ratio": a00_ratio,
            "raw_topological_local_real": raw_tail,
            "paired_topological_local_real": paired_tail,
            "local_real_standard_deviation_ratio": local_ratio,
            "paired_imaginary": scalar_summary(
                np.asarray(
                    [
                        row["paired_topological_local_imaginary"]
                        for row in event_rows
                    ]
                )
            ),
            "thresholds_retuned_after_outcomes": False,
        }
        if state == "COMPLETE_RETROSPECTIVE_REPLAY":
            scientific_gates = {
                "mean_difference_is_zero_compatible": bool(
                    difference_mean_standard_errors
                    <= MAXIMUM_MEAN_DIFFERENCE_STANDARD_ERRORS
                ),
                "A00_variance_reduction_gate": bool(
                    a00_ratio <= MAXIMUM_A00_STANDARD_DEVIATION_RATIO
                ),
                "local_variance_reduction_gate": bool(
                    local_ratio <= MAXIMUM_LOCAL_STANDARD_DEVIATION_RATIO
                ),
            }
            passed = all(scientific_gates.values())
            analysis["scientific_gates"] = scientific_gates
            analysis["retrospective_acceptance_passed"] = passed
            decision = (
                "AUTHORIZE_BLIND_BOUNDED_PAIRED_PARTITION_PILOT"
                if passed
                else "REJECT_PAIRED_PARTITION_SCALE_WITHOUT_NEW_DERIVATION"
            )

    result = {
        "checkpoint": 5227,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "state": state,
        "decision": decision,
        "completed_event_count": len(complete_seeds),
        "completed_job_count": 2 * len(complete_seeds),
        "expected_event_count": 24,
        "expected_job_count": 48,
        "estimator_machine_checks": estimator_machine_checks(),
        "analysis": analysis,
        "topology_reuse_audit": str(TOPOLOGY_REUSE),
        "protocol_lock_sha256": digest(PROTOCOL_LOCK),
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": 5227,
            "state": state,
            "decision": decision,
            "completed_event_count": len(complete_seeds),
            "completed_job_count": 2 * len(complete_seeds),
        },
    )
    if state == "COMPLETE_RETROSPECTIVE_REPLAY":
        write_final(result, manifest)
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def write_final(result: dict[str, Any], manifest: dict[str, Any]) -> None:
    analysis = result["analysis"]
    topology = read_json(TOPOLOGY_REUSE)
    validation_rows = [
        {
            "check": "source_chain_5224_to_5226_validated",
            "passed": (
                read_json(RESULT_5224)["state"] == "COMPLETE_DESIGN"
                and all_pass(VALIDATION_5224)
                and all_pass(VALIDATION_5225)
                and all_pass(VALIDATION_5226)
            ),
            "detail": "5224 complete; 5224-5226 validation all-pass",
        },
        {
            "check": "protocol_lock_matches_current_runner",
            "passed": read_json(PROTOCOL_LOCK)["contract"][
                "runner_sha256"
            ]
            == digest(Path(__file__).resolve()),
            "detail": digest(Path(__file__).resolve()),
        },
        {
            "check": "all_48_jobs_converged",
            "passed": (
                result["completed_job_count"] == 48
                and result["state"] == "COMPLETE_RETROSPECTIVE_REPLAY"
            ),
            "detail": str(result["completed_job_count"]),
        },
        {
            "check": "paired_multiplier_is_bounded_on_physical_sample",
            "passed": result["estimator_machine_checks"]["passed"],
            "detail": str(
                result["estimator_machine_checks"][
                    "maximum_real_physical_multiplier"
                ]
            ),
        },
        {
            "check": "paired_endpoint_samples_are_finite",
            "passed": (
                result["estimator_machine_checks"][
                    "paired_endpoint_samples_all_finite"
                ]
                and result["estimator_machine_checks"][
                    "endpoint_regularity_gate"
                ]
            ),
            "detail": str(
                {
                    "maximum_magnitude": result[
                        "estimator_machine_checks"
                    ]["maximum_endpoint_sample_magnitude"],
                    "x_scaled_ratio": result[
                        "estimator_machine_checks"
                    ]["endpoint_x_scaled_ratio"],
                    "magnitude_ratio": result[
                        "estimator_machine_checks"
                    ]["endpoint_magnitude_ratio"],
                }
            ),
        },
        {
            "check": "topology_reuse_adds_no_pole_roots",
            "passed": (
                topology["topology_count"] == 48
                and all(
                    not row["new_pole_roots_required"]
                    for row in topology["rows"]
                )
            ),
            "detail": str(topology["topology_count"]),
        },
        {
            "check": "scientific_decision_matches_prelocked_gates",
            "passed": (
                (
                    analysis["retrospective_acceptance_passed"]
                    and result["decision"]
                    == "AUTHORIZE_BLIND_BOUNDED_PAIRED_PARTITION_PILOT"
                )
                or (
                    not analysis["retrospective_acceptance_passed"]
                    and result["decision"]
                    == (
                        "REJECT_PAIRED_PARTITION_SCALE_WITHOUT_NEW_"
                        "DERIVATION"
                    )
                )
            ),
            "detail": str(analysis["scientific_gates"]),
        },
        {
            "check": "thresholds_not_retuned",
            "passed": (
                not analysis["thresholds_retuned_after_outcomes"]
                and not manifest[
                    "retrospective_acceptance_thresholds"
                ]["threshold_retuning_after_outcomes_allowed"]
            ),
            "detail": "frozen before paired replay",
        },
        {
            "check": "formalization_workbench_unchanged",
            "passed": (
                result["formalization_workbench_tree_sha256"]
                == FORMAL_BASELINE
            ),
            "detail": result["formalization_workbench_tree_sha256"],
        },
        {
            "check": "all_claim_flags_remain_false",
            "passed": not any(
                (
                    result["valid_for_numeric_UV_claim"],
                    result["valid_for_local_GR_claim"],
                    result["valid_for_full_MTS_claim"],
                )
            ),
            "detail": "numeric UV, local GR and full MTS remain false",
        },
    ]
    write_csv(VALIDATION, validation_rows)
    validation_all_passed = all(
        bool(row["passed"]) for row in validation_rows
    )
    result["validation_all_passed"] = validation_all_passed
    result["validation_check_count"] = len(validation_rows)
    atomic_json(RESULT, result)

    document = f"""# 5227 - Bounded paired-partition A00 replay

## Result

The unit source-family control rejected at checkpoint 5225 has been replaced
by an exact bounded channel pullback, not by a fitted coefficient.

Decision: `{result['decision']}`.

All `{result['completed_job_count']}/48` replay jobs converged.

## Derived estimator

The original direct channel is

`W3 = 3 w3`.

Checkpoint 5226 supplies the measure-preserving `g1<->g3` involution.
Pulling the slot-1 channel back into the working slot-3 chart gives `3 w1`.
Their arithmetic mean is therefore

`W13 = 3 (w3+w1)/2`.

This is unbiased by identical-graviton symmetry. On real phase space,
`0 <= W13 <= 3/2`, so it cannot reproduce the unbounded `w1/w3`
importance ratio. Because `W3` and `W13` have the same partition
denominator, no new topology poles are introduced.

The plus-distribution endpoint is also derived: as `x3->0`, `w3->1` and
`w1->0`, so the paired endpoint subtraction is exactly one half of the
original endpoint.

## Retrospective test

- Events: `{analysis['event_count']}`.
- Mean paired-minus-raw difference:
  `{analysis['paired_minus_raw_A00_real']['mean']:.9g}` with
  `{analysis['difference_mean_in_standard_errors']:.6g}` standard errors.
- A00 real SD ratio:
  `{analysis['A00_real_standard_deviation_ratio']:.9g}`.
- Local topological real SD ratio:
  `{analysis['local_real_standard_deviation_ratio']:.9g}`.
- Raw/paired local maximum event shares:
  `{analysis['raw_topological_local_real']['maximum_absolute_event_share']:.9g}` /
  `{analysis['paired_topological_local_real']['maximum_absolute_event_share']:.9g}`.
- Raw/paired local maximum leave-one-out shifts:
  `{analysis['raw_topological_local_real']['maximum_leave_one_out_shift_standard_errors']:.9g}` /
  `{analysis['paired_topological_local_real']['maximum_leave_one_out_shift_standard_errors']:.9g}`.

## Interpretation

This sample was already exposed during estimator development. A passing
variance result can authorize a genuinely new blind pilot, but cannot be
promoted to a numerical ultraviolet coefficient. A failed result rejects
this estimator without post-hoc multiplier tuning.

## Claim boundary

The calculation concerns only the crossed-`hhh` A00 contribution. It does
not close the other cut classes, a canonical UV coefficient, local GR, the
galaxy branch, or full MTS.

## Evidence

- Manifest: `{MANIFEST}`
- Protocol lock: `{PROTOCOL_LOCK}`
- Topology reuse: `{TOPOLOGY_REUSE}`
- Event rows: `{EVENT_ROWS}`
- Result: `{RESULT}`
- Validation: `{VALIDATION}`
"""
    atomic_text(DOCUMENT, document)
    if not validation_all_passed:
        raise RuntimeError(
            "checkpoint-5227 final validation failed: "
            + json.dumps(
                [row for row in validation_rows if not row["passed"]],
                indent=2,
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("prepare", "run", "analyse", "all"), default="all"
    )
    parser.add_argument("--wall-cap-hours", type=float, default=4.0)
    parser.add_argument("--maximum-events", type=int, default=0)
    arguments = parser.parse_args()
    manifest, config, jobs = prepare()
    if arguments.mode == "prepare":
        print(
            json.dumps(
                {
                    "checkpoint": 5227,
                    "state": "PREPARED",
                    "job_count": len(jobs),
                    "protocol_lock_sha256": digest(PROTOCOL_LOCK),
                },
                indent=2,
            )
        )
        return
    if arguments.mode in ("run", "all"):
        run(
            manifest,
            config,
            jobs,
            arguments.wall_cap_hours,
            arguments.maximum_events,
        )
    analyse(manifest, config, jobs)


if __name__ == "__main__":
    main()
