from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
MANIFEST = POST / "source-intake" / "functional_rg" / "5076" / "locked_central_anchor_pilot_manifest.json"
PILOT_RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v6"
SOURCE = POST / "source-intake" / "functional_rg" / "5080"
LOCK_JSON = SOURCE / "fresh_pilot_analysis_lock_v6.json"
RESULT_JSON = SOURCE / "fresh_pilot_analysis.json"
CHANNEL_CSV = SOURCE / "fresh_pilot_channels.csv"
EVENT_CSV = SOURCE / "fresh_pilot_event_costs.csv"
JACKKNIFE_CSV = SOURCE / "fresh_pilot_jackknife.csv"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5080_VALIDATION.csv"
MARKER = "MTS_5080_LOCKED_FRESH_PILOT_ANALYSIS"
REVISION = "outward-contour-fixed-control-analysis-lock-v6"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EFFICIENCY_THRESHOLD = 0.8
EXECUTION_CAP_HOURS = 10.0


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5077 = load_module("mts_5077_for_5080", SCRIPT_5077)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def analysis_lock() -> dict[str, Any]:
    manifest = read_json(MANIFEST)
    config = M5077.make_config(manifest, PILOT_RUN.name)
    jobs = M5077.pilot_jobs(config, manifest)
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "analysis_script_path": str(Path(__file__).resolve()),
        "analysis_script_sha256": digest(Path(__file__).resolve()),
        "pilot_run_path": str(PILOT_RUN),
        "pilot_config_digest": config["config_digest"],
        "pilot_schedule_digest": M5077.M5036.canonical_digest(jobs),
        "expected_job_count": len(jobs),
        "residue_certificate_policy": config["residue_certificate_policy"],
        "high_seeds": manifest["fresh_high_scramble_seeds"],
        "low_seeds": manifest["fresh_low_scramble_seeds"],
        "high_units": manifest["high_units"],
        "low_units": manifest["low_units"],
        "high_observable": "P[2*R_primary(E020)-R_primary(E040)]",
        "paired_low_observable": "P[R_coarse(E040)]",
        "independent_low_observable": "P[R_coarse(E040)]",
        "projector": "orthogonal complement of shape 1-z^2",
        "fixed_control": {
            "real_channels": 1.0,
            "imaginary_channels": 0.0,
            "fit_from_fresh_data": False,
        },
        "estimator": "mean_high(high-fixed_B*paired_low)+fixed_B*mean_low(independent_low)",
        "variance_estimator": "sample covariance of four corrections / 4 plus sample covariance of twelve low contributions / 12",
        "primary_decision_metric": "maximum realized-cost target-normalized score divided by fresh high-only base score",
        "primary_decision_threshold": EFFICIENCY_THRESHOLD,
        "runtime_cap_hours": EXECUTION_CAP_HOURS,
        "decision_rule": "PASS only if all 360 kernels converge, realized runtime is at most ten hours, and the locked score ratio is below 0.8",
        "delete_one_high_and_low_panels": "diagnostic only; no post-hoc threshold",
        "target_central_values_used": False,
        "lock_created_before_complete_pilot_analysis": True,
        "valid_for_full_MTS_claim": False,
    }


def job_value(path: Path) -> complex:
    row = read_json(path)
    if row.get("status") != "COMPLETED_CONVERGED":
        raise RuntimeError(f"pilot job is not converged: {path}")
    value = row["normalized_direct_D_hhh_over_G3"]
    return complex(float(value["real"]), float(value["imaginary"]))


def event_arguments(
    run_directory: Path,
    event_id: str,
    epsilon_id: str,
    profile: str,
    base_ids: list[str],
) -> dict[tuple[str, str], complex]:
    return {
        (base_id, "value"): job_value(
            run_directory
            / "jobs"
            / f"{epsilon_id}__{event_id}__{base_id}__{profile}.json"
        )
        for base_id in base_ids
    }


def event_cost(
    run_directory: Path,
    event_id: str,
    job_specs: list[tuple[str, str]],
    base_ids: list[str],
) -> float:
    total = 0.0
    for epsilon_id, profile in job_specs:
        for base_id in base_ids:
            path = (
                run_directory
                / "jobs"
                / f"{epsilon_id}__{event_id}__{base_id}__{profile}.json"
            )
            total += float(read_json(path)["job_runtime_seconds"])
    return total


def channel_labels(config: dict[str, Any]) -> list[str]:
    return [
        *[f"real_z{float(value):+.1f}" for value in config["physical_cosines"]],
        *[
            f"imag_z{float(value):+.1f}"
            for value in config["physical_cosines"]
        ],
    ]


def covariance(values: np.ndarray) -> np.ndarray:
    return np.atleast_2d(np.cov(values, rowvar=False, ddof=1))


def finite_array(value: np.ndarray) -> bool:
    return bool(np.all(np.isfinite(value)))


def analyze(lock: dict[str, Any]) -> dict[str, Any]:
    completion = PILOT_RUN / "COMPLETED.json"
    if not completion.exists():
        raise RuntimeError("the bounded pilot is not complete")
    if lock["analysis_script_sha256"] != digest(Path(__file__).resolve()):
        raise RuntimeError("analysis script changed after its pre-analysis lock")
    completion_row = read_json(completion)
    if completion_row["completed_converged"] != 360:
        raise RuntimeError("the bounded pilot matrix is incomplete")
    manifest = read_json(MANIFEST)
    config = read_json(PILOT_RUN / "config.json")
    if config["config_digest"] != lock["pilot_config_digest"]:
        raise RuntimeError("pilot config differs from the pre-analysis lock")
    base_ids = [row["argument_id"] for row in config["base_arguments"]]
    event_lookup = M5077.M5036.event_lookup(config)
    high_seeds = [int(value) for value in manifest["fresh_high_scramble_seeds"]]
    low_seeds = [int(value) for value in manifest["fresh_low_scramble_seeds"]]
    seed_to_event = {int(row["seed"]): row["event_id"] for row in event_lookup.values()}
    high_rows = []
    event_rows: list[dict[str, Any]] = []
    for seed in high_seeds:
        event_id = seed_to_event[seed]
        e040 = event_arguments(
            PILOT_RUN, event_id, "E040", "primary24", base_ids
        )
        e020 = event_arguments(
            PILOT_RUN, event_id, "E020", "primary24", base_ids
        )
        paired_low = event_arguments(
            PILOT_RUN, event_id, "E040", "coarse12", base_ids
        )
        e040_residual = M5077.M5043.cyclic_nonlocal(config, e040)
        e020_residual = M5077.M5043.cyclic_nonlocal(config, e020)
        low_residual = M5077.M5043.cyclic_nonlocal(config, paired_low)
        high = 2.0 * e020_residual - e040_residual
        high_channels = np.concatenate((high.real, high.imag))
        correction = np.concatenate(
            ((high - low_residual).real, high.imag)
        )
        low_contribution = np.concatenate(
            (low_residual.real, np.zeros(5, dtype=float))
        )
        high_cost = event_cost(
            PILOT_RUN,
            event_id,
            [("E040", "primary24"), ("E020", "primary24")],
            base_ids,
        )
        correction_cost = high_cost + event_cost(
            PILOT_RUN,
            event_id,
            [("E040", "coarse12")],
            base_ids,
        )
        high_rows.append((high_channels, correction, low_contribution))
        event_rows.append(
            {
                "role": "high_and_paired_low",
                "seed": seed,
                "event_id": event_id,
                "high_only_runtime_seconds": high_cost,
                "locked_correction_runtime_seconds": correction_cost,
                "low_only_runtime_seconds": "",
            }
        )
    independent_low_rows = []
    for seed in low_seeds:
        event_id = seed_to_event[seed]
        low_arguments = event_arguments(
            PILOT_RUN, event_id, "E040", "coarse12", base_ids
        )
        low_residual = M5077.M5043.cyclic_nonlocal(config, low_arguments)
        independent_low_rows.append(
            np.concatenate((low_residual.real, np.zeros(5, dtype=float)))
        )
        low_cost = event_cost(
            PILOT_RUN,
            event_id,
            [("E040", "coarse12")],
            base_ids,
        )
        event_rows.append(
            {
                "role": "independent_low",
                "seed": seed,
                "event_id": event_id,
                "high_only_runtime_seconds": "",
                "locked_correction_runtime_seconds": "",
                "low_only_runtime_seconds": low_cost,
            }
        )
    high = np.stack([row[0] for row in high_rows])
    correction = np.stack([row[1] for row in high_rows])
    paired_low_contribution = np.stack([row[2] for row in high_rows])
    independent_low = np.stack(independent_low_rows)
    high_units = high.shape[0]
    low_units = independent_low.shape[0]
    estimate = np.mean(correction, axis=0) + np.mean(independent_low, axis=0)
    high_estimate = np.mean(high, axis=0)
    correction_covariance = covariance(correction)
    low_covariance = covariance(independent_low)
    high_covariance = covariance(high)
    estimator_covariance = (
        correction_covariance / high_units + low_covariance / low_units
    )
    estimator_se = np.sqrt(np.maximum(np.diag(estimator_covariance), 0.0))
    high_se = np.sqrt(np.maximum(np.diag(high_covariance) / high_units, 0.0))
    variance_high = np.diag(high_covariance)
    variance_correction = np.diag(correction_covariance)
    variance_low = np.diag(low_covariance)
    high_cost = float(
        np.mean(
            [float(row["high_only_runtime_seconds"]) for row in event_rows[:4]]
        )
    )
    correction_cost = float(
        np.mean(
            [
                float(row["locked_correction_runtime_seconds"])
                for row in event_rows[:4]
            ]
        )
    )
    low_cost = float(
        np.mean(
            [
                float(row["low_only_runtime_seconds"])
                for row in event_rows[4:]
            ]
        )
    )
    real_margins = np.asarray(
        [
            float(row["target_equivalence_margin"])
            for row in config["target_precision_budgets"]
        ]
    )
    margins = np.concatenate((real_margins, real_margins))
    base_score = float(np.max(np.sqrt(variance_high * high_cost) / margins))
    low_to_high_ratio = low_units / high_units
    variance_cost = (
        variance_correction + variance_low / low_to_high_ratio
    ) * (correction_cost + low_to_high_ratio * low_cost)
    normalized_components = (
        np.sqrt(np.maximum(variance_cost, 0.0)) / margins / base_score
    )
    score_ratio = float(np.max(normalized_components))
    realized_runtime_hours = float(
        (
            high_units * correction_cost
            + low_units * low_cost
        )
        / 3600.0
    )
    direct_recorded_runtime_hours = float(
        sum(
            float(read_json(path)["job_runtime_seconds"])
            for path in (PILOT_RUN / "jobs").glob("*.json")
        )
        / 3600.0
    )
    locked_gate_passed = (
        score_ratio < EFFICIENCY_THRESHOLD
        and direct_recorded_runtime_hours <= EXECUTION_CAP_HOURS
    )
    jackknife_rows = []
    safe_se = np.where(estimator_se > 0.0, estimator_se, math.inf)
    for index, seed in enumerate(high_seeds):
        candidate = (
            np.mean(np.delete(correction, index, axis=0), axis=0)
            + np.mean(independent_low, axis=0)
        )
        shift = np.abs(candidate - estimate) / safe_se
        jackknife_rows.append(
            {
                "deletion_role": "high",
                "deleted_seed": seed,
                "maximum_shift_in_full_standard_errors": float(np.max(shift)),
                "worst_channel_index": int(np.argmax(shift)),
            }
        )
    for index, seed in enumerate(low_seeds):
        candidate = (
            np.mean(correction, axis=0)
            + np.mean(np.delete(independent_low, index, axis=0), axis=0)
        )
        shift = np.abs(candidate - estimate) / safe_se
        jackknife_rows.append(
            {
                "deletion_role": "low",
                "deleted_seed": seed,
                "maximum_shift_in_full_standard_errors": float(np.max(shift)),
                "worst_channel_index": int(np.argmax(shift)),
            }
        )
    labels = channel_labels(config)
    channel_rows = []
    for index, label in enumerate(labels):
        channel_rows.append(
            {
                "channel": label,
                "active_control": index < 5,
                "estimate": float(estimate[index]),
                "standard_error": float(estimator_se[index]),
                "high_only_estimate": float(high_estimate[index]),
                "high_only_standard_error": float(high_se[index]),
                "same_high_sample_se_ratio": float(
                    estimator_se[index] / high_se[index]
                )
                if high_se[index] > 0.0
                else math.inf,
                "target_margin": float(margins[index]),
                "standard_error_over_margin": float(
                    estimator_se[index] / margins[index]
                ),
                "realized_cost_normalized_component_score_ratio": float(
                    normalized_components[index]
                ),
            }
        )
    write_rows(CHANNEL_CSV, channel_rows)
    write_rows(EVENT_CSV, event_rows)
    write_rows(JACKKNIFE_CSV, jackknife_rows)
    all_arrays_finite = all(
        finite_array(value)
        for value in (
            high,
            correction,
            paired_low_contribution,
            independent_low,
            estimate,
            estimator_covariance,
            normalized_components,
        )
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "analysis_lock_path": str(LOCK_JSON),
        "analysis_lock_sha256": digest(LOCK_JSON),
        "analysis_script_sha256": digest(Path(__file__).resolve()),
        "pilot_completion_path": str(completion),
        "pilot_completion_sha256": digest(completion),
        "pilot_matrix_complete": completion_row["completed_converged"] == 360,
        "high_units": high_units,
        "low_units": low_units,
        "high_seeds": high_seeds,
        "low_seeds": low_seeds,
        "channel_order": labels,
        "fixed_control_real": 1.0,
        "fixed_control_imaginary": 0.0,
        "fresh_data_used_to_fit_control": False,
        "mean_high_only_runtime_seconds": high_cost,
        "mean_locked_correction_runtime_seconds": correction_cost,
        "mean_low_only_runtime_seconds": low_cost,
        "realized_runtime_hours_from_event_costs": realized_runtime_hours,
        "direct_recorded_job_runtime_hours": direct_recorded_runtime_hours,
        "high_only_base_score": base_score,
        "realized_cost_normalized_component_score_ratios": normalized_components.tolist(),
        "realized_cost_normalized_score_ratio": score_ratio,
        "predeclared_efficiency_threshold": EFFICIENCY_THRESHOLD,
        "maximum_estimator_standard_error_over_margin": float(
            np.max(estimator_se / margins)
        ),
        "maximum_high_only_standard_error_over_margin": float(
            np.max(high_se / margins)
        ),
        "maximum_delete_one_shift_in_full_standard_errors": max(
            row["maximum_shift_in_full_standard_errors"]
            for row in jackknife_rows
        ),
        "locked_numerical_efficiency_gate_passed": locked_gate_passed,
        "decision": "LOCKED_FRESH_PILOT_PASSES"
        if locked_gate_passed
        else "LOCKED_FRESH_PILOT_DOES_NOT_PASS",
        "all_arrays_finite": all_arrays_finite,
        "target_central_values_used": False,
        "result_scope": "fresh numerical estimator efficiency only",
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        (
            "analysis_lock_unchanged",
            lock["analysis_script_sha256"] == result["analysis_script_sha256"],
            result["analysis_script_sha256"],
        ),
        (
            "pilot_matrix_complete",
            result["pilot_matrix_complete"],
            "360/360 completed converged jobs required",
        ),
        (
            "sample_counts_locked",
            high_units == 4 and low_units == 12,
            f"high={high_units}; low={low_units}",
        ),
        (
            "seed_lists_locked",
            high_seeds == lock["high_seeds"] and low_seeds == lock["low_seeds"],
            "fresh seed lists match the pre-analysis lock",
        ),
        (
            "fixed_control_not_fit",
            not result["fresh_data_used_to_fit_control"],
            "B_real=1 and B_imag=0",
        ),
        (
            "all_arrays_finite",
            result["all_arrays_finite"],
            "all estimator arrays are finite",
        ),
        (
            "runtime_accounting_consistent",
            abs(realized_runtime_hours - direct_recorded_runtime_hours)
            <= max(1.0e-9, 1.0e-9 * direct_recorded_runtime_hours),
            f"event={realized_runtime_hours}; direct={direct_recorded_runtime_hours}",
        ),
        (
            "decision_rule_consistent",
            result["locked_numerical_efficiency_gate_passed"]
            == (
                score_ratio < EFFICIENCY_THRESHOLD
                and direct_recorded_runtime_hours <= EXECUTION_CAP_HOURS
            ),
            f"score={score_ratio}; runtime_h={direct_recorded_runtime_hours}",
        ),
        (
            "target_central_values_not_used",
            not result["target_central_values_used"],
            "no target central value enters the estimator or decision",
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "pilot efficiency does not establish the full theory",
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
                    "check_id": f"V5080_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5080 validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("lock", "analyze"), default="lock")
    arguments = parser.parse_args()
    if arguments.mode == "lock":
        if LOCK_JSON.exists():
            existing = read_json(LOCK_JSON)
            if existing["analysis_script_sha256"] != digest(Path(__file__).resolve()):
                raise RuntimeError("an analysis lock already exists for different code")
            result = existing
        else:
            result = analysis_lock()
            atomic_json(LOCK_JSON, result)
    else:
        if not LOCK_JSON.exists():
            raise RuntimeError("create the analysis lock before analysis")
        result = analyze(read_json(LOCK_JSON))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
