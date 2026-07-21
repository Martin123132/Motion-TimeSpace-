from __future__ import annotations

import argparse
import importlib.util
import json
import math
import statistics
import time
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5036 = POST / "scripts" / "Y5_R2FR_5036_paired_full_vector_ladder.py"
SOURCE_5036_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5036"
    / "runs"
    / "paired_full_vector_s2_v1"
)
SOURCE_5036_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5036"
    / "paired_full_vector_results.json"
)
SOURCE_5036_COMPLETE = SOURCE_5036_RUN / "COMPLETE"
SOURCE = POST / "source-intake" / "functional_rg" / "5037"
RUNS = SOURCE / "runs"
RESULT_JSON = SOURCE / "paired_outer_precision_results.json"
VECTOR_CSV = SOURCE / "epsilon_cyclic_vector.csv"
DECOMPOSITION_CSV = SOURCE / "local_nonlocal_decomposition.csv"
PAIRED_CSV = SOURCE / "paired_vector_convergence.csv"
TARGET_CSV = SOURCE / "epsilon_zero_target_comparison.csv"
GATE_CSV = SOURCE / "outer_precision_gate.csv"
REFLECTION_CSV = SOURCE / "reflection_control.csv"
PRECISION_CSV = SOURCE / "outer_precision_diagnostic.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
MARKER = "MTS_5037_PAIRED_OUTER_PRECISION_REFLECTION_CONTROL"
SCHEMA_REVISION = "four-scramble-paired-outer-precision-reflection-control-v1"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5036 = load_module("mts_5036_for_5037", SCRIPT_5036)
M5036.MARKER = MARKER
M5036.SCHEMA_REVISION = SCHEMA_REVISION
M5036.M5035.MARKER = MARKER
M5036.M5035.M5034.MARKER = MARKER
M5036.SOURCE = SOURCE
M5036.RUNS = RUNS
M5036.RESULT_JSON = RESULT_JSON
M5036.VECTOR_CSV = VECTOR_CSV
M5036.DECOMPOSITION_CSV = DECOMPOSITION_CSV
M5036.PAIRED_CSV = PAIRED_CSV
M5036.TARGET_CSV = TARGET_CSV
M5036.GATE_CSV = GATE_CSV
M5036.PROVENANCE = PROVENANCE


def make_config(arguments: argparse.Namespace) -> dict[str, Any]:
    config = M5036.make_config(arguments)
    config.pop("config_digest", None)
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = SCHEMA_REVISION
    config["source_reuse"] = {
        "complete_two_scramble_full_matrix": str(SOURCE_5036_RUN),
        "four_scramble_central_ladder": str(M5036.SOURCE_5035_RUN),
        "exact_event_argument_epsilon_tier_match_required": True,
        "source_job_sha256_required": True,
    }
    config["outer_precision_contract"] = {
        "baseline_scrambles": [503401, 503402],
        "new_scrambles": [503403, 503404],
        "minimum_scrambles_for_precision_smoke": 4,
        "minimum_scrambles_for_target_verdict": 8,
        "paired_linear_diagnostic": "2*C(0.02)-C(0.04)",
        "target_fitted": False,
        "production_precision_claimed": False,
    }
    config["reflection_contract"] = {
        "pairs": [[-0.6, 0.6], [-0.3, 0.3]],
        "even_component": "R_even=(R(-z)+R(+z))/2",
        "odd_component": "R_odd=(R(-z)-R(+z))/2",
        "symmetry_imposed": False,
        "odd_component_zero_assumed": False,
    }
    config["execution_order"] = {
        "first": "complete epsilon 0.04 and 0.02 for each new scramble",
        "second": "complete epsilon 0.08 for the same scrambles",
        "reason": "obtain an independent outer-precision diagnostic before extending the three-level convergence population",
    }
    config["source_files"].update(
        {
            str(SCRIPT_5036): M5036.file_digest(SCRIPT_5036),
            str(SOURCE_5036_RUN / "config.json"): M5036.file_digest(
                SOURCE_5036_RUN / "config.json"
            ),
            str(SOURCE_5036_RESULT): M5036.file_digest(SOURCE_5036_RESULT),
            str(SOURCE_5036_COMPLETE): M5036.file_digest(SOURCE_5036_COMPLETE),
            str(Path(__file__).resolve()): M5036.file_digest(Path(__file__).resolve()),
        }
    )
    config["target_fitted"] = False
    config["epsilon_limit_complete"] = False
    config["production_precision_complete"] = False
    config["valid_for_full_MTS_claim"] = False
    config["config_digest"] = M5036.canonical_digest(config)
    return config


def source_maps() -> list[tuple[str, dict[Any, Any], dict[Any, Any]]]:
    map_5036, events_5036 = M5036.source_job_map(
        SOURCE_5036_RUN, "5036_complete_two_scramble_full_matrix"
    )
    map_5035, events_5035 = M5036.source_job_map(
        M5036.SOURCE_5035_RUN, "5035_four_scramble_central_ladder"
    )
    return [
        ("5036_complete_two_scramble_full_matrix", map_5036, events_5036),
        ("5035_four_scramble_central_ladder", map_5035, events_5035),
    ]


def reusable_source(
    expected: dict[str, Any],
    config: dict[str, Any],
    mappings: list[tuple[str, dict[Any, Any], dict[Any, Any]]],
) -> tuple[dict[str, Any], Path, str] | None:
    events = M5036.event_lookup(config)
    arguments = M5036.argument_lookup(config)
    event = events[expected["event_id"]]
    argument = arguments[expected["argument_id"]]
    key = (
        M5036.canonical_float(expected["evaluation_epsilon"]),
        int(event["seed"]),
        int(event["sample_index"]),
        M5036.canonical_float(argument["argument"]),
        expected["tier"],
    )
    for source_label, mapping, source_events in mappings:
        source_entry = mapping.get(key)
        if source_entry is None:
            continue
        source_job, source_path, _ = source_entry
        source_point = source_events.get(
            (int(event["seed"]), int(event["sample_index"]))
        )
        if source_point != event["unit_cube_point"]:
            raise RuntimeError(f"paired Sobol event mismatch for {expected['job_key']}")
        return source_job, source_path, source_label
    return None


def import_reusable_jobs(
    run_directory: Path,
    config: dict[str, Any],
    jobs: dict[str, dict[str, Any]],
) -> dict[str, int]:
    mappings = source_maps()
    events = M5036.event_lookup(config)
    arguments = M5036.argument_lookup(config)
    imported_counts = {source_label: 0 for source_label, _, _ in mappings}
    for expected in M5036.expected_jobs(config):
        if expected["job_key"] in jobs:
            continue
        source_entry = reusable_source(expected, config, mappings)
        if source_entry is None:
            continue
        source_job, source_path, source_label = source_entry
        event = events[expected["event_id"]]
        argument = arguments[expected["argument_id"]]
        direct = M5036.complex_from_row(
            source_job["normalized_direct_D_hhh_over_G3"]
        )
        if not M5036.finite_complex(direct):
            raise RuntimeError(f"non-finite source job {source_path}")
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
            "topology_class_descriptor": source_job["topology_class_descriptor"],
            "topology_signature_digest": source_job["topology_signature_digest"],
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
                "source_job_sha256": M5036.file_digest(source_path),
                "source_job_key": source_job["job_key"],
                "upstream_import": source_job.get("imported_from"),
            },
            "upstream_radius_contract": source_job.get("residue_radius_contract"),
            "job_runtime_seconds": 0.0,
            "completed_at": M5036.utc_now(),
            "valid_for_full_MTS_claim": False,
        }
        M5036.atomic_json(M5036.job_path(run_directory, expected["job_key"]), result)
        jobs[expected["job_key"]] = result
        imported_counts[source_label] += 1
    if sum(imported_counts.values()):
        M5036.append_log(run_directory, f"exact imports {imported_counts}")
    return imported_counts


def linear_event_decompositions(
    config: dict[str, Any], summary: dict[str, Any]
) -> list[dict[str, Any]]:
    per_seed = {
        (row["epsilon_id"], int(row["seed"])): np.asarray(
            [M5036.complex_from_row(value) for value in row["cyclic_vector"]],
            dtype=np.complex128,
        )
        for row in summary["cyclic_vectors_per_seed"]
        if row["cyclic_vector"] is not None
        and row["completed_samples"] == row["expected_samples"]
    }
    larger_id = config["epsilon_ids"][-2]
    smaller_id = config["epsilon_ids"][-1]
    shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
    rows: list[dict[str, Any]] = []
    for seed in config["seeds"]:
        larger_key = (larger_id, int(seed))
        smaller_key = (smaller_id, int(seed))
        if larger_key not in per_seed or smaller_key not in per_seed:
            continue
        vector = 2.0 * per_seed[smaller_key] - per_seed[larger_key]
        coefficient, residual, orthogonality = M5036.project_vector(vector, shape)
        rows.append(
            {
                "seed": int(seed),
                "vector": vector,
                "local_coefficient": coefficient,
                "nonlocal_residual": residual,
                "projection_orthogonality": orthogonality,
            }
        )
    return rows


def serialized_estimate(values: list[complex]) -> dict[str, Any] | None:
    return M5036.aggregate_complex(values) if values else None


def reflection_diagnostic(
    config: dict[str, Any], linear_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    physical_cosines = [float(value) for value in config["physical_cosines"]]
    index = {round(value, 12): position for position, value in enumerate(physical_cosines)}
    target = {
        round(float(row["physical_s_channel_cosine"]), 12): float(
            row["required_matched_hhh_nonlocal_cyclic_D_over_G3"]
        )
        for row in config["target_rows"]
    }
    pair_rows: list[dict[str, Any]] = []
    for absolute_cosine in (0.6, 0.3):
        negative_index = index[round(-absolute_cosine, 12)]
        positive_index = index[round(absolute_cosine, 12)]
        even_values = [
            complex(
                (row["nonlocal_residual"][negative_index]
                + row["nonlocal_residual"][positive_index])
                / 2.0
            )
            for row in linear_rows
        ]
        odd_values = [
            complex(
                (row["nonlocal_residual"][negative_index]
                - row["nonlocal_residual"][positive_index])
                / 2.0
            )
            for row in linear_rows
        ]
        target_even = (
            target[round(-absolute_cosine, 12)]
            + target[round(absolute_cosine, 12)]
        ) / 2.0
        target_odd = (
            target[round(-absolute_cosine, 12)]
            - target[round(absolute_cosine, 12)]
        ) / 2.0
        odd_estimate = serialized_estimate(odd_values)
        pair_rows.append(
            {
                "absolute_cosine": absolute_cosine,
                "even_estimate": serialized_estimate(even_values),
                "odd_estimate": odd_estimate,
                "fixed_target_even": target_even,
                "fixed_target_odd": target_odd,
                "predicted_odd_minus_target_odd": (
                    odd_estimate["mean"]["real"] - target_odd
                    if odd_estimate is not None
                    else None
                ),
            }
        )
    center_index = index[0.0]
    center_values = [
        complex(row["nonlocal_residual"][center_index]) for row in linear_rows
    ]
    return {
        "available": len(linear_rows) >= 2,
        "paired_scrambles": len(linear_rows),
        "model": "eventwise nonlocal residual of 2*C(0.02)-C(0.04)",
        "pair_rows": pair_rows,
        "center_estimate": serialized_estimate(center_values),
        "reflection_symmetry_imposed": False,
        "odd_component_zero_assumed": False,
        "reflection_zero_claimed": False,
        "valid_for_full_MTS_claim": False,
    }


def precision_diagnostic(
    config: dict[str, Any],
    summary: dict[str, Any],
    linear_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    baseline_seeds = set(config["outer_precision_contract"]["baseline_scrambles"])
    baseline = [row for row in linear_rows if row["seed"] in baseline_seeds]
    current = linear_rows
    baseline_local = serialized_estimate(
        [complex(row["local_coefficient"]) for row in baseline]
    )
    current_local = serialized_estimate(
        [complex(row["local_coefficient"]) for row in current]
    )
    target = {
        round(float(row["physical_s_channel_cosine"]), 12): float(
            row["required_matched_hhh_nonlocal_cyclic_D_over_G3"]
        )
        for row in config["target_rows"]
    }
    component_rows: list[dict[str, Any]] = []
    se_ratios: list[float] = []
    for component_index, cosine in enumerate(config["physical_cosines"]):
        baseline_estimate = serialized_estimate(
            [
                complex(row["nonlocal_residual"][component_index])
                for row in baseline
            ]
        )
        current_estimate = serialized_estimate(
            [
                complex(row["nonlocal_residual"][component_index])
                for row in current
            ]
        )
        ratio = None
        standardized_residual = None
        if baseline_estimate is not None and current_estimate is not None:
            baseline_error = baseline_estimate["real_standard_error"]
            current_error = current_estimate["real_standard_error"]
            if baseline_error not in (None, 0.0) and current_error is not None:
                ratio = float(current_error / baseline_error)
                if math.isfinite(ratio):
                    se_ratios.append(ratio)
            if current_error not in (None, 0.0):
                target_value = target[round(float(cosine), 12)]
                standardized_residual = float(
                    (current_estimate["mean"]["real"] - target_value)
                    / current_error
                )
        component_rows.append(
            {
                "physical_s_channel_cosine": float(cosine),
                "baseline_two_scramble_estimate": baseline_estimate,
                "current_estimate": current_estimate,
                "current_to_baseline_real_se_ratio": ratio,
                "fixed_target": target[round(float(cosine), 12)],
                "target_residual_over_current_se": standardized_residual,
            }
        )
    completed_scrambles = len(current)
    minimum_smoke = int(
        config["outer_precision_contract"]["minimum_scrambles_for_precision_smoke"]
    )
    minimum_verdict = int(
        config["outer_precision_contract"]["minimum_scrambles_for_target_verdict"]
    )
    finite_current = all(
        row["current_estimate"] is not None
        and math.isfinite(float(row["current_estimate"]["mean"]["real"]))
        and math.isfinite(float(row["current_estimate"]["mean"]["imaginary"]))
        for row in component_rows
    )
    return {
        "available": completed_scrambles >= 2,
        "completed_paired_scrambles": completed_scrambles,
        "baseline_paired_scrambles": len(baseline),
        "minimum_scrambles_for_precision_smoke": minimum_smoke,
        "minimum_scrambles_for_target_verdict": minimum_verdict,
        "baseline_local_coefficient": baseline_local,
        "current_local_coefficient": current_local,
        "component_rows": component_rows,
        "median_current_to_baseline_real_se_ratio": (
            statistics.median(se_ratios) if se_ratios else None
        ),
        "minimum_four_scramble_precision_smoke": (
            completed_scrambles >= minimum_smoke and finite_current
        ),
        "fixed_target_verdict_ready": (
            completed_scrambles >= minimum_verdict
            and finite_current
            and summary["epsilon_limit_complete"]
        ),
        "target_fitted": False,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }


def augment_summary(
    config: dict[str, Any], summary: dict[str, Any]
) -> dict[str, Any]:
    linear_rows = linear_event_decompositions(config, summary)
    reflection = reflection_diagnostic(config, linear_rows)
    precision = precision_diagnostic(config, summary, linear_rows)
    summary["reflection_diagnostic"] = reflection
    summary["outer_precision_diagnostic"] = precision
    summary["gate"]["four_scramble_linear_matrix_complete"] = (
        precision["completed_paired_scrambles"] == 4
    )
    summary["gate"]["reflection_control_diagnostic_complete"] = (
        reflection["available"] and reflection["paired_scrambles"] == 4
    )
    summary["gate"]["minimum_four_scramble_precision_smoke"] = precision[
        "minimum_four_scramble_precision_smoke"
    ]
    summary["gate"]["fixed_target_verdict_ready"] = precision[
        "fixed_target_verdict_ready"
    ]
    summary["gate"]["reflection_symmetry_imposed"] = False
    summary["gate"]["production_precision_complete"] = False
    summary["gate"]["valid_for_full_MTS_claim"] = False
    summary["target_fitted"] = False
    summary["epsilon_limit_complete"] = False
    summary["production_precision_complete"] = False
    summary["valid_for_full_MTS_claim"] = False
    return summary


def write_augmented_status(
    run_directory: Path,
    config: dict[str, Any],
    jobs: dict[str, dict[str, Any]],
    state: str,
    started: float,
) -> dict[str, Any]:
    summary = M5036.write_status(run_directory, config, jobs, state, started)
    summary = augment_summary(config, summary)
    M5036.atomic_json(run_directory / "partial_results.json", summary)
    return summary


def write_extra_artifacts(
    config: dict[str, Any], summary: dict[str, Any], run_directory: Path
) -> None:
    reflection_rows: list[dict[str, Any]] = []
    for row in summary["reflection_diagnostic"]["pair_rows"]:
        even = row["even_estimate"]
        odd = row["odd_estimate"]
        reflection_rows.append(
            {
                "absolute_cosine": row["absolute_cosine"],
                "paired_scrambles": summary["reflection_diagnostic"]["paired_scrambles"],
                "even_mean_real": even["mean"]["real"] if even else "",
                "even_real_standard_error": even["real_standard_error"] if even else "",
                "odd_mean_real": odd["mean"]["real"] if odd else "",
                "odd_real_standard_error": odd["real_standard_error"] if odd else "",
                "fixed_target_even": row["fixed_target_even"],
                "fixed_target_odd": row["fixed_target_odd"],
                "predicted_odd_minus_target_odd": row[
                    "predicted_odd_minus_target_odd"
                ],
                "symmetry_imposed": False,
            }
        )
    M5036.write_csv(
        REFLECTION_CSV,
        reflection_rows,
        [
            "absolute_cosine",
            "paired_scrambles",
            "even_mean_real",
            "even_real_standard_error",
            "odd_mean_real",
            "odd_real_standard_error",
            "fixed_target_even",
            "fixed_target_odd",
            "predicted_odd_minus_target_odd",
            "symmetry_imposed",
        ],
    )
    precision_rows: list[dict[str, Any]] = []
    precision = summary["outer_precision_diagnostic"]
    for row in precision["component_rows"]:
        baseline = row["baseline_two_scramble_estimate"]
        current = row["current_estimate"]
        precision_rows.append(
            {
                "physical_s_channel_cosine": row["physical_s_channel_cosine"],
                "baseline_scrambles": precision["baseline_paired_scrambles"],
                "current_scrambles": precision["completed_paired_scrambles"],
                "baseline_mean_real": baseline["mean"]["real"] if baseline else "",
                "baseline_real_standard_error": baseline["real_standard_error"] if baseline else "",
                "current_mean_real": current["mean"]["real"] if current else "",
                "current_real_standard_error": current["real_standard_error"] if current else "",
                "current_to_baseline_real_se_ratio": row[
                    "current_to_baseline_real_se_ratio"
                ],
                "fixed_target": row["fixed_target"],
                "target_residual_over_current_se": row[
                    "target_residual_over_current_se"
                ],
                "target_fitted": False,
            }
        )
    M5036.write_csv(
        PRECISION_CSV,
        precision_rows,
        [
            "physical_s_channel_cosine",
            "baseline_scrambles",
            "current_scrambles",
            "baseline_mean_real",
            "baseline_real_standard_error",
            "current_mean_real",
            "current_real_standard_error",
            "current_to_baseline_real_se_ratio",
            "fixed_target",
            "target_residual_over_current_se",
            "target_fitted",
        ],
    )
    M5036.atomic_text(
        PROVENANCE,
        f"""# 5037 provenance

- Marker: `{MARKER}`.
- Run directory: `{run_directory}`.
- Config digest: `{config['config_digest']}`.
- Complete two-scramble source: `post-checkpoint-work/source-intake/functional_rg/5036/runs/paired_full_vector_s2_v1`.
- Four-scramble central source: `post-checkpoint-work/source-intake/functional_rg/5035/runs/central_eps008_004_002_s4_v1`.
- Shrinking-radius rule: `post-checkpoint-work/scripts/Y5_R2FR_5035_pair_local_residue_radius_repair.py`.
- Fixed comparison rows: `post-checkpoint-work/source-intake/functional_rg/5018/known_master_without_hhh_and_matched_hhh_target.csv`.
- Existing jobs are accepted only on exact epsilon, event, argument and tier identity with a source-job SHA-256.
- Every new kernel retains its own canonical projective Feynman homotopy and the v4 shrinking-radius residue rule.
- The local/nonlocal split is eventwise; reflection is measured after that split and is never imposed.
- The fixed 5018 target is loaded after decomposition and is never fitted.
- Four scrambles are a minimum precision smoke, not production precision or a full-MTS claim.
""",
    )


def write_checkpoint_artifacts(
    config: dict[str, Any], summary: dict[str, Any], run_directory: Path
) -> None:
    M5036.write_checkpoint_artifacts(config, summary, run_directory)
    write_extra_artifacts(config, summary, run_directory)


def execution_order(
    config: dict[str, Any], expected: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    new_seeds = [int(seed) for seed in config["seeds"][2:]]
    epsilon_ids = {
        round(float(epsilon), 12): epsilon_id
        for epsilon_id, epsilon in zip(config["epsilon_ids"], config["epsilons"])
    }
    phases: list[tuple[int, str]] = []
    for seed in new_seeds:
        phases.extend(
            [
                (seed, epsilon_ids[0.04]),
                (seed, epsilon_ids[0.02]),
            ]
        )
    for seed in new_seeds:
        phases.append((seed, epsilon_ids[0.08]))
    phase_index = {value: index for index, value in enumerate(phases)}
    event_seed = {
        row["event_id"]: int(row["seed"]) for row in config["events"]
    }
    base_index = {
        value: index
        for index, value in enumerate(M5036.ordered_base_argument_ids(config))
    }
    return sorted(
        expected,
        key=lambda row: (
            phase_index.get(
                (event_seed[row["event_id"]], row["epsilon_id"]), -1
            ),
            0 if row["tier"] == "primary24" else 1,
            base_index[row["base_argument_id"]],
        ),
    )


def dry_run_summary(config: dict[str, Any]) -> dict[str, Any]:
    expected = M5036.expected_jobs(config)
    mappings = source_maps()
    reusable = [
        row for row in expected if reusable_source(row, config, mappings) is not None
    ]
    return {
        "checkpoint_marker": MARKER,
        "dry_run": True,
        "run_id": config["run_id"],
        "config_digest": config["config_digest"],
        "epsilons": config["epsilons"],
        "seeds": config["seeds"],
        "expected_jobs": len(expected),
        "expected_primary_jobs": sum(row["tier"] == "primary24" for row in expected),
        "expected_audit_jobs": sum(row["tier"] == "audit32" for row in expected),
        "source_locked_imports": len(reusable),
        "new_kernels_required": len(expected) - len(reusable),
        "target_fitted": False,
        "reflection_symmetry_imposed": False,
        "valid_for_full_MTS_claim": False,
    }


def run(arguments: argparse.Namespace) -> dict[str, Any]:
    config = make_config(arguments)
    expected = M5036.expected_jobs(config)
    if arguments.dry_run:
        return dry_run_summary(config)
    run_directory = RUNS / config["run_id"]
    config = M5036.load_or_create_config(run_directory, config)
    started = time.monotonic()
    jobs = M5036.load_jobs(run_directory)
    imported = import_reusable_jobs(run_directory, config, jobs)
    write_augmented_status(run_directory, config, jobs, "RUNNING", started)
    M5036.append_log(
        run_directory,
        f"invocation start terminal={len(jobs)} expected={len(expected)} imports={imported} max_wall={arguments.max_wall_seconds}",
    )
    new_kernels = 0
    state = "COMPLETE"
    M5036.N5030.chamber_residue_catalog = M5036.MREPAIR.repaired_chamber_residue_catalog
    try:
        for job in execution_order(config, expected):
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
            M5036.append_log(run_directory, f"starting {job['job_key']}")
            result = M5036.execute_new_job(run_directory, config, job)
            jobs[job["job_key"]] = result
            new_kernels += 1
            M5036.append_log(
                run_directory,
                f"finished {job['job_key']} status={result['status']} seconds={result['job_runtime_seconds']:.3f}",
            )
            write_augmented_status(run_directory, config, jobs, "RUNNING", started)
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
        M5036.N5030.chamber_residue_catalog = M5036.ORIGINAL_CATALOG
    expected_keys = {row["job_key"] for row in expected}
    if len(set(jobs) & expected_keys) < len(expected_keys) and state == "COMPLETE":
        state = "PAUSED"
    summary = write_augmented_status(run_directory, config, jobs, state, started)
    if state == "COMPLETE":
        M5036.atomic_text(
            run_directory / "COMPLETE",
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "completed_at": M5036.utc_now(),
                    "failed_jobs": summary["failed_jobs"],
                    "unconverged_jobs": summary["unconverged_jobs"],
                },
                indent=2,
            )
            + "\n",
        )
    else:
        (run_directory / "COMPLETE").unlink(missing_ok=True)
    M5036.append_log(
        run_directory,
        f"invocation stop state={state} terminal={summary['terminal_jobs']} remaining={summary['remaining_jobs']}",
    )
    write_checkpoint_artifacts(config, summary, run_directory)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="paired_outer_precision_s4_v1")
    parser.add_argument("--physical-cosines", default="-0.6,-0.3,0,0.3,0.6")
    parser.add_argument("--epsilons", default="0.08,0.04,0.02")
    parser.add_argument("--seeds", default="503401,503402,503403,503404")
    parser.add_argument("--power", type=int, default=0)
    parser.add_argument("--topology-steps", type=int, default=96)
    parser.add_argument("--topology-maximum-steps", type=int, default=49152)
    parser.add_argument("--regulator", type=float, default=1.0e-3)
    parser.add_argument("--boundary-tracking-steps", type=int, default=64)
    parser.add_argument("--max-wall-seconds", type=float, default=9000.0)
    parser.add_argument("--max-new-kernels", type=int)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_wall_seconds <= 0.0:
        raise ValueError("max wall seconds must be positive")
    result = run(arguments)
    if result.get("dry_run"):
        console_result = result
    else:
        precision = result["outer_precision_diagnostic"]
        console_result = {
            "checkpoint_marker": MARKER,
            "run_state": result["run_state"],
            "expected_jobs": result["expected_jobs"],
            "terminal_jobs": result["terminal_jobs"],
            "remaining_jobs": result["remaining_jobs"],
            "imported_jobs": result["imported_jobs"],
            "computed_converged_jobs": result["computed_converged_jobs"],
            "failed_jobs": result["failed_jobs"],
            "unconverged_jobs": result["unconverged_jobs"],
            "completed_paired_scrambles": precision[
                "completed_paired_scrambles"
            ],
            "minimum_four_scramble_precision_smoke": precision[
                "minimum_four_scramble_precision_smoke"
            ],
            "fixed_target_verdict_ready": precision[
                "fixed_target_verdict_ready"
            ],
            "valid_for_full_MTS_claim": False,
        }
    print(json.dumps(console_result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
