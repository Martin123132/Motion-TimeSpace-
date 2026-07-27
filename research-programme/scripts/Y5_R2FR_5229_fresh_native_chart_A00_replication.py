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
SOURCE_5228 = FUNCTIONAL_RG / "5228"
SOURCE = FUNCTIONAL_RG / "5229"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5224 = (
    POST / "scripts" / "Y5_R2FR_5224_replacement_scaled_controlled_run.py"
)
SCRIPT_5228 = (
    POST / "scripts" / "Y5_R2FR_5228_one_chart_cross_sector_blend_no_go.py"
)
CONFIG_5224 = SOURCE_5224 / "frozen_replacement_config.json"
RESULT_5224 = SOURCE_5224 / "replacement_scaled_controlled_results.json"
CONTROL_ROWS_5224 = SOURCE_5224 / "replacement_A00_control_rows.csv"
VALIDATION_5224 = RESIDUALS / "P8_Y5_BRR545_5224_VALIDATION.csv"
RESULT_5228 = SOURCE_5228 / "one_chart_cross_sector_blend_no_go.json"
VALIDATION_5228 = RESIDUALS / "P8_Y5_BRR545_5228_VALIDATION.csv"
SOURCE_CLASSIFIER_CACHE = (
    SOURCE_5224
    / "runs"
    / "replacement_scaled_controlled_v1"
    / "grouped-classifier-cache"
)

RUN_DIRECTORY = SOURCE / "runs" / "fresh_native_chart_A00_replication"
CLASSIFIER_CACHE = RUN_DIRECTORY / "grouped-classifier-cache"
MANIFEST = SOURCE / "frozen_native_chart_A00_manifest.json"
CONFIG = SOURCE / "frozen_native_chart_A00_config.json"
SCHEDULE = SOURCE / "frozen_native_chart_A00_schedule.csv"
PROTOCOL_LOCK = SOURCE / "frozen_native_chart_A00_protocol_lock.json"
STATUS = RUN_DIRECTORY / "status.json"
EVENT_ROWS = SOURCE / "fresh_native_chart_A00_event_rows.csv"
RESULT = SOURCE / "fresh_native_chart_A00_results.json"
DOCUMENT = POST / "5229-Y5-R2FR-fresh-native-chart-A00-replication.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5229_VALIDATION.csv"

MARKER = "MTS_5229_FRESH_NATIVE_CHART_A00_REPLICATION"
REVISION = "fresh-native-sector-safe-A00-replication-v1"
RUN_ID = "fresh_native_chart_A00_replication"
FRESH_SEEDS = tuple(range(731942001, 731942025))
PHYSICAL_A00_WEIGHT = -0.008
MAXIMUM_WALL_HOURS = 4.0
MAXIMUM_MEAN_DIFFERENCE_STANDARD_ERRORS = 2.0
MINIMUM_VARIANCE_RATIO = 0.25
MAXIMUM_VARIANCE_RATIO = 4.0
MAXIMUM_NEW_EVENT_SHARE = 0.40
MAXIMUM_NEW_LEAVE_ONE_OUT_SHIFT_STANDARD_ERRORS = 1.0
MAXIMUM_POOLED_EVENT_SHARE = 0.30
MAXIMUM_POOLED_STANDARD_ERROR_RATIO = 0.80
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5224 = load_module(SCRIPT_5224, "mts_5224_for_5229")
M5212 = M5224.M5212
M5036 = M5212.M5077.M5036


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


def all_pass(path: Path) -> bool:
    return all(
        row["passed"].strip().lower() == "true" for row in read_csv(path)
    )


def complex_from_row(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def source_paths() -> list[Path]:
    return [
        Path(__file__).resolve(),
        SCRIPT_5224,
        SCRIPT_5228,
        CONFIG_5224,
        RESULT_5224,
        CONTROL_ROWS_5224,
        VALIDATION_5224,
        RESULT_5228,
        VALIDATION_5228,
    ]


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


def source_A00_rows() -> list[dict[str, str]]:
    return read_csv(CONTROL_ROWS_5224)


def source_A00_summary() -> dict[str, Any]:
    rows = source_A00_rows()
    values = np.asarray([float(row["raw_A00_real"]) for row in rows])
    seeds = [int(row["seed"]) for row in rows]
    return {
        "scalar": scalar_summary(values),
        "tails": M5212.scalar_distribution_diagnostics(values, seeds),
        "seeds": seeds,
    }


def make_manifest() -> dict[str, Any]:
    result_5224 = read_json(RESULT_5224)
    result_5228 = read_json(RESULT_5228)
    if not (
        result_5224["state"] == "COMPLETE_DESIGN"
        and result_5224["counts"]["completed_converged"] == 520
        and all_pass(VALIDATION_5224)
        and result_5228["decision"]
        == (
            "REJECT_NONZERO_CONSTANT_CROSS_SECTOR_MIXTURES_IN_ONE_"
            "SOFT_CHART"
        )
        and result_5228["validation_all_passed"]
        and all_pass(VALIDATION_5228)
    ):
        raise RuntimeError("checkpoint-5224/5228 source chain is not closed")
    old_seeds = {
        int(row["seed"]) for row in read_json(CONFIG_5224)["events"]
    }
    if old_seeds.intersection(FRESH_SEEDS):
        raise RuntimeError("fresh seed collision with checkpoint 5224")
    return {
        "checkpoint": 5229,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": RUN_ID,
        "locked_date": "2026-07-25",
        "source_outcomes_known_at_lock": True,
        "fresh_outcomes_present_at_lock": False,
        "fresh_seed_search_before_lock": {
            "range": [FRESH_SEEDS[0], FRESH_SEEDS[-1]],
            "searched_roots": [
                str(FUNCTIONAL_RG),
                str(POST / "scripts"),
            ],
            "prior_occurrences": 0,
        },
        "fresh_full_scramble_seeds": [],
        "fresh_topological_scramble_seeds": list(FRESH_SEEDS),
        "event_count": len(FRESH_SEEDS),
        "expected_job_count": 2 * len(FRESH_SEEDS),
        "epsilon_ids": ["E040", "E020"],
        "required_base_argument_ids": ["A00"],
        "profile": "primary24",
        "integrand": {
            "native_soft_slot": 3,
            "direct_weight": "3*w3",
            "cross_sector_blend": False,
            "source_family_control": False,
            "endpoint_subtraction_coefficient": 1.0,
            "physics_kernel_changed_from_5224_raw_A00": False,
        },
        "prelocked_scientific_gates": {
            "maximum_mean_difference_standard_errors": (
                MAXIMUM_MEAN_DIFFERENCE_STANDARD_ERRORS
            ),
            "variance_ratio_interval": [
                MINIMUM_VARIANCE_RATIO,
                MAXIMUM_VARIANCE_RATIO,
            ],
            "maximum_new_absolute_event_share": MAXIMUM_NEW_EVENT_SHARE,
            "maximum_new_leave_one_out_shift_standard_errors": (
                MAXIMUM_NEW_LEAVE_ONE_OUT_SHIFT_STANDARD_ERRORS
            ),
            "maximum_pooled_absolute_event_share": (
                MAXIMUM_POOLED_EVENT_SHARE
            ),
            "maximum_pooled_standard_error_ratio": (
                MAXIMUM_POOLED_STANDARD_ERROR_RATIO
            ),
            "retuning_after_outcomes_allowed": False,
        },
        "source_A00_summary": source_A00_summary(),
        "interpretation": (
            "fresh native-chart A00 replication only; passing gates "
            "authorizes pooling this A00 diagnostic and extending the "
            "unchanged design, not a UV coefficient claim"
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


def generated_event_config() -> dict[str, Any]:
    arguments = argparse.Namespace(
        run_id=RUN_ID,
        physical_cosines="-0.6,-0.3,0,0.3,0.6",
        epsilons="0.08,0.04,0.02",
        seeds=",".join(str(seed) for seed in FRESH_SEEDS),
        power=0,
        topology_steps=96,
        topology_maximum_steps=49152,
        regulator=1.0e-3,
        boundary_tracking_steps=64,
    )
    return M5036.make_config(arguments)


def make_config(manifest: dict[str, Any]) -> dict[str, Any]:
    config = read_json(CONFIG_5224)
    generated = generated_event_config()
    for key in (
        "audit_seed",
        "events",
        "power",
        "samples_per_seed",
        "seeds",
    ):
        config[key] = generated[key]
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = REVISION
    config["run_id"] = RUN_ID
    config["pilot_manifest"] = str(MANIFEST)
    config["pilot_manifest_digest"] = digest(MANIFEST)
    config["fresh_A00_control_contract"] = {
        "applied": False,
        "reason": (
            "checkpoint-5225 retired the unit control and checkpoint-5228 "
            "requires the native sector-safe raw estimator"
        ),
    }
    config["two_stratum_contract"] = {
        "full_seeds": [],
        "topological_seeds": list(FRESH_SEEDS),
        "required_base_argument_ids": ["A00"],
        "epsilon_ids": ["E040", "E020"],
        "profile": "primary24",
        "pole_model_and_smooth_must_remain_paired": True,
        "unsafe_reciprocal_pairs_evaluate_both_roots": True,
        "pilot_only": True,
    }
    config["topology_cache_scope_correction"] = {
        "manager_run_directory": str(RUN_DIRECTORY),
        "source_checkpoint": 5229,
        "topology_generating_contract_unchanged": True,
    }
    config["source_files"][str(Path(__file__).resolve())] = digest(
        Path(__file__).resolve()
    )
    config["source_files"][str(RESULT_5228)] = digest(RESULT_5228)
    config.pop("config_digest", None)
    config["config_digest"] = M5036.canonical_digest(config)
    return config


def jobs_for(
    config: dict[str, Any], manifest: dict[str, Any]
) -> list[dict[str, Any]]:
    jobs = M5212.build_schedule(config, manifest)
    if len(jobs) != 48:
        raise RuntimeError(f"expected 48 jobs, got {len(jobs)}")
    return jobs


def schedule_rows(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"schedule_index": index, **job}
        for index, job in enumerate(jobs, start=1)
    ]


def copy_classifier_cache() -> None:
    CLASSIFIER_CACHE.mkdir(parents=True, exist_ok=True)
    if not SOURCE_CLASSIFIER_CACHE.is_dir():
        raise FileNotFoundError(SOURCE_CLASSIFIER_CACHE)
    for source in SOURCE_CLASSIFIER_CACHE.rglob("*.json"):
        target = CLASSIFIER_CACHE / source.relative_to(
            SOURCE_CLASSIFIER_CACHE
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if digest(target) != digest(source):
                raise RuntimeError(f"classifier cache collision: {target}")
        else:
            shutil.copy2(source, target)


def prepare() -> tuple[
    dict[str, Any], dict[str, Any], list[dict[str, Any]]
]:
    for path in source_paths():
        if not path.is_file():
            raise FileNotFoundError(path)
    SOURCE.mkdir(parents=True, exist_ok=True)
    RUN_DIRECTORY.mkdir(parents=True, exist_ok=True)
    if MANIFEST.exists():
        manifest = read_json(MANIFEST)
    else:
        if list(RUN_DIRECTORY.glob("topological-jobs/*.json")):
            raise RuntimeError("fresh outcomes exist before manifest lock")
        manifest = make_manifest()
        atomic_json(MANIFEST, manifest)
    if CONFIG.exists():
        config = read_json(CONFIG)
    else:
        config = make_config(manifest)
        atomic_json(CONFIG, config)
    jobs = jobs_for(config, manifest)
    if not SCHEDULE.exists():
        write_csv(SCHEDULE, schedule_rows(jobs))
    contract = {
        "manifest_sha256": digest(MANIFEST),
        "config_sha256": digest(CONFIG),
        "schedule_sha256": digest(SCHEDULE),
        "runner_sha256": digest(Path(__file__).resolve()),
        "fresh_seed_digest": canonical_digest(list(FRESH_SEEDS)),
        "expected_job_count": len(jobs),
        "integrand_revision": manifest["integrand"],
        "scientific_gate_digest": canonical_digest(
            manifest["prelocked_scientific_gates"]
        ),
    }
    if PROTOCOL_LOCK.exists():
        lock = read_json(PROTOCOL_LOCK)
        if lock["contract"] != contract:
            raise RuntimeError("checkpoint-5229 protocol changed after lock")
    else:
        if list(RUN_DIRECTORY.glob("topological-jobs/*.json")):
            raise RuntimeError("fresh outcomes exist before protocol lock")
        atomic_json(
            PROTOCOL_LOCK,
            {
                "checkpoint": 5229,
                "checkpoint_marker": MARKER,
                "contract": contract,
                "fresh_outcomes_present_at_lock": False,
                "threshold_retuning_after_outcomes_allowed": False,
            },
        )
    copy_classifier_cache()
    return manifest, config, jobs


def install_runtime(config: dict[str, Any]) -> Any:
    M5224.RUN_DIRECTORY = RUN_DIRECTORY
    M5224.CLASSIFIER_CACHE = CLASSIFIER_CACHE
    M5224.RUNTIME_ROWS.clear()
    return M5224.install_runtime(config)


def completed_event_seeds(
    config: dict[str, Any], jobs: list[dict[str, Any]]
) -> list[int]:
    return [
        seed
        for seed in FRESH_SEEDS
        if all(
            (
                M5212.cached_result(RUN_DIRECTORY, config, job) or {}
            ).get("status")
            == "COMPLETED_CONVERGED"
            for job in jobs
            if int(job["seed"]) == seed
        )
    ]


def run(
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
    wall_cap_hours: float,
    maximum_events: int,
) -> None:
    if not (0.0 < wall_cap_hours <= MAXIMUM_WALL_HOURS):
        raise ValueError("wall cap must lie in (0,4] hours")
    manager = install_runtime(config)
    started = time.monotonic()
    newly_completed = 0
    for seed in FRESH_SEEDS:
        event_jobs = [job for job in jobs if int(job["seed"]) == seed]
        if all(
            (
                M5212.cached_result(RUN_DIRECTORY, config, job) or {}
            ).get("status")
            == "COMPLETED_CONVERGED"
            for job in event_jobs
        ):
            continue
        if maximum_events and newly_completed >= maximum_events:
            break
        for job in event_jobs:
            if M5212.cached_result(RUN_DIRECTORY, config, job) is not None:
                continue
            row = M5212.execute_job(
                RUN_DIRECTORY, config, manager, job
            )
            row.update(
                {
                    "checkpoint_marker": MARKER,
                    "revision": REVISION,
                    "native_soft_slot": 3,
                    "cross_sector_blend": False,
                    "source_family_control": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            atomic_json(M5212.output_path(RUN_DIRECTORY, job), row)
            atomic_json(
                STATUS,
                {
                    "checkpoint": 5229,
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
                    f"fresh replication stopped at {job['job_key']}: {row}"
                )
            if (
                time.monotonic() - started
            ) / 3600.0 >= wall_cap_hours:
                return
        newly_completed += 1


def analyse(
    manifest: dict[str, Any],
    config: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    complete_seeds = completed_event_seeds(config, jobs)
    event_rows: list[dict[str, Any]] = []
    for seed in complete_seeds:
        selected = {
            job["epsilon_id"]: job
            for job in jobs
            if int(job["seed"]) == seed
        }
        values = {
            epsilon: complex_from_row(
                read_json(
                    M5212.output_path(RUN_DIRECTORY, selected[epsilon])
                )["normalized_topological_D_hhh_over_G3"]
            )
            for epsilon in ("E040", "E020")
        }
        a00 = PHYSICAL_A00_WEIGHT * (
            2.0 * values["E020"] - values["E040"]
        )
        event = next(
            row for row in config["events"] if int(row["seed"]) == seed
        )
        event_rows.append(
            {
                "seed": seed,
                "event_id": event["event_id"],
                "soft_energy": event["soft_energy"],
                "soft_cosine": event["soft_cosine"],
                "decay_cosine": event["decay_cosine"],
                "E040_real": values["E040"].real,
                "E040_imaginary": values["E040"].imag,
                "E020_real": values["E020"].real,
                "E020_imaginary": values["E020"].imag,
                "A00_real": a00.real,
                "A00_imaginary": a00.imag,
                "valid_for_numeric_UV_claim": False,
            }
        )
    if event_rows:
        write_csv(EVENT_ROWS, event_rows)

    state = (
        "COMPLETE_FRESH_NATIVE_CHART_REPLICATION"
        if len(complete_seeds) == len(FRESH_SEEDS)
        else "PARTIAL_FRESH_NATIVE_CHART_REPLICATION"
    )
    analysis: dict[str, Any] | None = None
    decision = "CONTINUE_FRESH_NATIVE_CHART_REPLICATION"
    if len(event_rows) >= 2:
        old_rows = source_A00_rows()
        old_real = np.asarray(
            [float(row["raw_A00_real"]) for row in old_rows]
        )
        old_imaginary = np.asarray(
            [float(row["raw_A00_imaginary"]) for row in old_rows]
        )
        old_seeds = [int(row["seed"]) for row in old_rows]
        new_real = np.asarray([float(row["A00_real"]) for row in event_rows])
        new_imaginary = np.asarray(
            [float(row["A00_imaginary"]) for row in event_rows]
        )
        pooled_real = np.concatenate((old_real, new_real))
        pooled_imaginary = np.concatenate((old_imaginary, new_imaginary))
        pooled_seeds = old_seeds + complete_seeds
        old_summary = scalar_summary(old_real)
        new_summary = scalar_summary(new_real)
        pooled_summary = scalar_summary(pooled_real)
        mean_difference_se = math.sqrt(
            float(old_summary["standard_error"]) ** 2
            + float(new_summary["standard_error"]) ** 2
        )
        mean_difference_standard_errors = abs(
            float(new_summary["mean"]) - float(old_summary["mean"])
        ) / max(mean_difference_se, 1.0e-300)
        variance_ratio = float(
            np.var(new_real, ddof=1) / np.var(old_real, ddof=1)
        )
        old_tails = M5212.scalar_distribution_diagnostics(
            old_real, old_seeds
        )
        new_tails = M5212.scalar_distribution_diagnostics(
            new_real, complete_seeds
        )
        pooled_tails = M5212.scalar_distribution_diagnostics(
            pooled_real, pooled_seeds
        )
        pooled_standard_error_ratio = float(
            float(pooled_summary["standard_error"])
            / float(old_summary["standard_error"])
        )
        scientific_gates = {
            "mean_compatibility": bool(
                mean_difference_standard_errors
                <= MAXIMUM_MEAN_DIFFERENCE_STANDARD_ERRORS
            ),
            "variance_compatibility": bool(
                MINIMUM_VARIANCE_RATIO
                <= variance_ratio
                <= MAXIMUM_VARIANCE_RATIO
            ),
            "new_event_share": bool(
                new_tails["maximum_absolute_event_share"]
                <= MAXIMUM_NEW_EVENT_SHARE
            ),
            "new_leave_one_out": bool(
                new_tails["maximum_leave_one_out_shift_standard_errors"]
                <= MAXIMUM_NEW_LEAVE_ONE_OUT_SHIFT_STANDARD_ERRORS
            ),
            "pooled_event_share": bool(
                pooled_tails["maximum_absolute_event_share"]
                <= MAXIMUM_POOLED_EVENT_SHARE
            ),
            "pooled_precision": bool(
                pooled_standard_error_ratio
                <= MAXIMUM_POOLED_STANDARD_ERROR_RATIO
            ),
        }
        pooling_authorized = all(scientific_gates.values())
        analysis = {
            "old_A00_real": old_summary,
            "new_A00_real": new_summary,
            "pooled_A00_real": pooled_summary,
            "old_A00_tails": old_tails,
            "new_A00_tails": new_tails,
            "pooled_A00_tails": pooled_tails,
            "old_A00_imaginary": scalar_summary(old_imaginary),
            "new_A00_imaginary": scalar_summary(new_imaginary),
            "pooled_A00_imaginary": scalar_summary(pooled_imaginary),
            "mean_difference_standard_errors": (
                mean_difference_standard_errors
            ),
            "new_to_old_variance_ratio": variance_ratio,
            "pooled_to_old_standard_error_ratio": (
                pooled_standard_error_ratio
            ),
            "scientific_gates": scientific_gates,
            "pooling_authorized": pooling_authorized,
            "thresholds_retuned_after_outcomes": False,
        }
        if state == "COMPLETE_FRESH_NATIVE_CHART_REPLICATION":
            decision = (
                "AUTHORIZE_NATIVE_CHART_A00_POOL_AND_FULL_VECTOR_EXTENSION"
                if pooling_authorized
                else "KEEP_A00_TRANCHES_SEPARATE_AND_DIAGNOSE_NATIVE_TAILS"
            )

    result = {
        "checkpoint": 5229,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "state": state,
        "decision": decision,
        "completed_event_count": len(complete_seeds),
        "completed_job_count": 2 * len(complete_seeds),
        "expected_event_count": len(FRESH_SEEDS),
        "expected_job_count": 2 * len(FRESH_SEEDS),
        "analysis": analysis,
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
            "checkpoint": 5229,
            "state": state,
            "decision": decision,
            "completed_event_count": len(complete_seeds),
            "completed_job_count": 2 * len(complete_seeds),
        },
    )
    if state == "COMPLETE_FRESH_NATIVE_CHART_REPLICATION":
        write_final(result, manifest, jobs)
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def write_final(
    result: dict[str, Any],
    manifest: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> None:
    analysis = result["analysis"]
    job_rows = [
        read_json(M5212.output_path(RUN_DIRECTORY, job)) for job in jobs
    ]
    expected_decision = (
        "AUTHORIZE_NATIVE_CHART_A00_POOL_AND_FULL_VECTOR_EXTENSION"
        if analysis["pooling_authorized"]
        else "KEEP_A00_TRANCHES_SEPARATE_AND_DIAGNOSE_NATIVE_TAILS"
    )
    validation_rows = [
        {
            "check": "source_chain_5224_and_5228_validated",
            "passed": (
                read_json(RESULT_5224)["state"] == "COMPLETE_DESIGN"
                and all_pass(VALIDATION_5224)
                and read_json(RESULT_5228)["validation_all_passed"]
                and all_pass(VALIDATION_5228)
            ),
            "detail": "5224 and 5228 all-pass",
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
            "check": "fresh_seeds_are_disjoint_from_source",
            "passed": not set(FRESH_SEEDS).intersection(
                int(row["seed"]) for row in read_json(CONFIG_5224)["events"]
            ),
            "detail": f"{FRESH_SEEDS[0]}..{FRESH_SEEDS[-1]}",
        },
        {
            "check": "all_48_jobs_converged",
            "passed": (
                len(job_rows) == 48
                and all(
                    row["status"] == "COMPLETED_CONVERGED"
                    for row in job_rows
                )
            ),
            "detail": str(len(job_rows)),
        },
        {
            "check": "native_sector_safe_integrand_preserved",
            "passed": (
                manifest["integrand"]["direct_weight"] == "3*w3"
                and not manifest["integrand"]["cross_sector_blend"]
                and not manifest["integrand"]["source_family_control"]
                and manifest["integrand"][
                    "endpoint_subtraction_coefficient"
                ]
                == 1.0
            ),
            "detail": str(manifest["integrand"]),
        },
        {
            "check": "scientific_decision_matches_prelocked_gates",
            "passed": result["decision"] == expected_decision,
            "detail": str(analysis["scientific_gates"]),
        },
        {
            "check": "thresholds_not_retuned",
            "passed": (
                not analysis["thresholds_retuned_after_outcomes"]
                and not manifest["prelocked_scientific_gates"][
                    "retuning_after_outcomes_allowed"
                ]
            ),
            "detail": "frozen before fresh outcomes",
        },
        {
            "check": "event_rows_are_complete_and_numeric",
            "passed": (
                len(read_csv(EVENT_ROWS)) == 24
                and all(
                    math.isfinite(float(row["A00_real"]))
                    and math.isfinite(float(row["A00_imaginary"]))
                    for row in read_csv(EVENT_ROWS)
                )
            ),
            "detail": "24 finite rows",
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
    validation_all_passed = all(
        bool(row["passed"]) for row in validation_rows
    )
    write_csv(VALIDATION, validation_rows)
    result["validation_all_passed"] = validation_all_passed
    result["validation_check_count"] = len(validation_rows)
    atomic_json(RESULT, result)

    document = f"""# 5229 - Fresh native-chart A00 replication

## Result

Checkpoint 5228 ruled out constant cross-sector mixtures in one soft chart.
This checkpoint therefore changed no physics kernel: it bought a genuinely
fresh native slot-3 replication using the original `3 w3` sector weight.

Decision: `{result['decision']}`.

All `{result['completed_job_count']}/{result['expected_job_count']}` jobs
converged.

## Frozen design

- Fresh seeds: `{FRESH_SEEDS[0]}` through `{FRESH_SEEDS[-1]}`.
- Fresh events: `{result['completed_event_count']}`.
- Arguments: `A00` at `E040` and `E020`.
- Cross-sector blend: none.
- Source-family control: none.
- Threshold retuning: forbidden.

## Replication comparison

- Old A00 mean / SE:
  `{analysis['old_A00_real']['mean']:.9g}` /
  `{analysis['old_A00_real']['standard_error']:.9g}`.
- New A00 mean / SE:
  `{analysis['new_A00_real']['mean']:.9g}` /
  `{analysis['new_A00_real']['standard_error']:.9g}`.
- Mean difference:
  `{analysis['mean_difference_standard_errors']:.9g}` combined standard
  errors.
- New/old variance ratio:
  `{analysis['new_to_old_variance_ratio']:.9g}`.
- Pooled A00 mean / SE:
  `{analysis['pooled_A00_real']['mean']:.9g}` /
  `{analysis['pooled_A00_real']['standard_error']:.9g}`.
- Pooled/original SE ratio:
  `{analysis['pooled_to_old_standard_error_ratio']:.9g}`.
- New/pooled maximum event shares:
  `{analysis['new_A00_tails']['maximum_absolute_event_share']:.9g}` /
  `{analysis['pooled_A00_tails']['maximum_absolute_event_share']:.9g}`.

## Interpretation

Passing every frozen gate authorizes pooling only this A00 diagnostic and
extending the unchanged native-chart design to the full vector. Failure
keeps the tranches separate and sends the actual native tails to diagnosis.
Neither outcome is a numerical ultraviolet coefficient.

## Claim boundary

The other angular arguments, full-vector smooth stratum, remaining cut
classes, canonical UV matching, local GR, galaxies and full MTS remain
open.

## Evidence

- Manifest: `{MANIFEST}`
- Config: `{CONFIG}`
- Protocol lock: `{PROTOCOL_LOCK}`
- Event rows: `{EVENT_ROWS}`
- Result: `{RESULT}`
- Validation: `{VALIDATION}`
"""
    atomic_text(DOCUMENT, document)
    if not validation_all_passed:
        raise RuntimeError(
            "checkpoint-5229 validation failed: "
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
                    "checkpoint": 5229,
                    "state": "PREPARED",
                    "event_count": len(FRESH_SEEDS),
                    "job_count": len(jobs),
                    "protocol_lock_sha256": digest(PROTOCOL_LOCK),
                },
                indent=2,
            )
        )
        return
    if arguments.mode in ("run", "all"):
        run(
            config,
            jobs,
            arguments.wall_cap_hours,
            arguments.maximum_events,
        )
    analyse(manifest, config, jobs)


if __name__ == "__main__":
    main()
