from __future__ import annotations

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
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5080 = POST / "scripts" / "Y5_R2FR_5080_locked_fresh_pilot_analysis.py"
DESIGN_LOCK = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5110"
    / "E020_primary_complex_control_design_lock.json"
)
DESIGN_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5110"
    / "E020_primary_complex_control_feasibility.json"
)
DESIGN_CHANNELS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5110"
    / "E020_primary_complex_control_channels.csv"
)
HIGH_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v12"
)
LOW_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5120"
RESULT_JSON = SOURCE / "locked_beta_one_complex_control_analysis.json"
CHANNEL_CSV = SOURCE / "locked_beta_one_complex_control_channels.csv"
EVENT_CSV = SOURCE / "locked_beta_one_complex_control_event_costs.csv"
JACKKNIFE_CSV = SOURCE / "locked_beta_one_complex_control_jackknife.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5120_VALIDATION.csv"
)
MARKER = "MTS_5120_LOCKED_BETA_ONE_COMPLEX_CONTROL_ANALYSIS"
REVISION = "realized-fixed-beta1-ratio3-complex-control-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5080 = load_module("mts_5080_for_5120", SCRIPT_5080)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def component_matrix(values: np.ndarray) -> np.ndarray:
    return np.concatenate((values.real, values.imag), axis=1)


def covariance(values: np.ndarray) -> np.ndarray:
    return np.atleast_2d(np.cov(values, rowvar=False, ddof=1))


def finite_array(value: np.ndarray) -> bool:
    return bool(np.all(np.isfinite(value)))


def main() -> None:
    required = [
        SCRIPT_5080,
        DESIGN_LOCK,
        DESIGN_RESULT,
        DESIGN_CHANNELS,
        HIGH_RUN / "config.json",
        HIGH_RUN / "COMPLETED.json",
        LOW_RUN / "config.json",
        LOW_RUN / "COMPLETED.json",
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5120 inputs: {missing}")
    lock = read_json(DESIGN_LOCK)
    design = read_json(DESIGN_RESULT)
    margin_rows = read_csv(DESIGN_CHANNELS)
    high_config = read_json(HIGH_RUN / "config.json")
    low_config = read_json(LOW_RUN / "config.json")
    high_completion = read_json(HIGH_RUN / "COMPLETED.json")
    low_completion = read_json(LOW_RUN / "COMPLETED.json")
    if digest(DESIGN_RESULT) != lock["source_result_sha256"]:
        raise RuntimeError("5110 design result changed after lock")
    if high_config["config_digest"] != lock["pilot_config_digest"]:
        raise RuntimeError("high config differs from the design lock")
    if low_config["config_digest"] != lock["pilot_config_digest"]:
        raise RuntimeError("low config differs from the design lock")
    if high_completion["completed_converged"] != 360:
        raise RuntimeError("high matrix is incomplete")
    if low_completion["completed_converged"] != 180:
        raise RuntimeError("control matrix is incomplete")
    beta = float(lock["fixed_beta_real"])
    ratio = float(lock["low_to_high_ratio"])
    threshold = float(lock["primary_decision_threshold"])
    runtime_cap_hours = float(lock["runtime_cap_hours"])
    if beta != 1.0 or float(lock["fixed_beta_imaginary"]) != 1.0:
        raise RuntimeError("locked complex beta is not one")
    high_seeds = [int(value) for value in lock["high_seeds"]]
    low_seeds = [int(value) for value in lock["low_seeds"]]
    if len(low_seeds) / len(high_seeds) != ratio:
        raise RuntimeError("realized sample allocation differs from the lock")
    base_ids = [str(row["argument_id"]) for row in high_config["base_arguments"]]
    event_lookup = M5080.M5077.M5036.event_lookup(high_config)
    seed_to_event = {
        int(row["seed"]): str(row["event_id"]) for row in event_lookup.values()
    }
    high_values: list[np.ndarray] = []
    paired_controls: list[np.ndarray] = []
    corrections: list[np.ndarray] = []
    high_costs: list[float] = []
    low_controls: list[np.ndarray] = []
    low_costs: list[float] = []
    event_rows: list[dict[str, Any]] = []
    for seed in high_seeds:
        event_id = seed_to_event[seed]
        epsilon_020 = M5080.event_arguments(
            HIGH_RUN, event_id, "E020", "primary24", base_ids
        )
        epsilon_040 = M5080.event_arguments(
            HIGH_RUN, event_id, "E040", "primary24", base_ids
        )
        control = M5080.M5077.M5043.cyclic_nonlocal(high_config, epsilon_020)
        epsilon_040_observable = M5080.M5077.M5043.cyclic_nonlocal(
            high_config, epsilon_040
        )
        high = 2.0 * control - epsilon_040_observable
        correction = high - beta * control
        cost = M5080.event_cost(
            HIGH_RUN,
            event_id,
            [("E020", "primary24"), ("E040", "primary24")],
            base_ids,
        )
        high_values.append(high)
        paired_controls.append(control)
        corrections.append(correction)
        high_costs.append(cost)
        event_rows.append(
            {
                "role": "high_and_paired_control",
                "seed": seed,
                "event_id": event_id,
                "accepted_runtime_seconds": cost,
            }
        )
    for seed in low_seeds:
        event_id = seed_to_event[seed]
        arguments = M5080.event_arguments(
            LOW_RUN, event_id, "E020", "primary24", base_ids
        )
        control = M5080.M5077.M5043.cyclic_nonlocal(low_config, arguments)
        cost = M5080.event_cost(
            LOW_RUN, event_id, [("E020", "primary24")], base_ids
        )
        low_controls.append(control)
        low_costs.append(cost)
        event_rows.append(
            {
                "role": "independent_control",
                "seed": seed,
                "event_id": event_id,
                "accepted_runtime_seconds": cost,
            }
        )
    high_complex = np.asarray(high_values, dtype=np.complex128)
    paired_complex = np.asarray(paired_controls, dtype=np.complex128)
    correction_complex = np.asarray(corrections, dtype=np.complex128)
    low_complex = np.asarray(low_controls, dtype=np.complex128)
    high = component_matrix(high_complex)
    paired = component_matrix(paired_complex)
    correction = component_matrix(correction_complex)
    independent = component_matrix(low_complex)
    high_units = high.shape[0]
    low_units = independent.shape[0]
    estimator = np.mean(correction, axis=0) + beta * np.mean(independent, axis=0)
    high_estimator = np.mean(high, axis=0)
    correction_covariance = covariance(correction)
    control_covariance = covariance(independent)
    high_covariance = covariance(high)
    estimator_covariance = (
        correction_covariance / high_units
        + beta * beta * control_covariance / low_units
    )
    estimator_se = np.sqrt(np.maximum(np.diag(estimator_covariance), 0.0))
    high_se = np.sqrt(np.maximum(np.diag(high_covariance) / high_units, 0.0))
    variance_high = np.diag(high_covariance)
    variance_correction = np.diag(correction_covariance)
    variance_control = np.diag(control_covariance)
    margins = np.asarray(
        [float(row["target_margin"]) for row in margin_rows], dtype=float
    )
    labels = [str(row["channel"]) for row in margin_rows]
    if len(labels) != 10 or margins.shape != (10,):
        raise RuntimeError("locked channel-margin schema changed")
    high_cost = float(np.mean(high_costs))
    control_cost = float(np.mean(low_costs))
    high_only_base_score = float(
        np.max(np.sqrt(variance_high * high_cost) / margins)
    )
    variance_cost = (
        variance_correction + beta * beta * variance_control / ratio
    ) * (high_cost + ratio * control_cost)
    normalized_components = (
        np.sqrt(np.maximum(variance_cost, 0.0))
        / margins
        / high_only_base_score
    )
    score_ratio = float(np.max(normalized_components))
    worst_index = int(np.argmax(normalized_components))
    accepted_runtime_seconds = float(sum(high_costs) + sum(low_costs))
    accepted_runtime_hours = accepted_runtime_seconds / 3600.0
    paired_identity_residual = float(
        np.max(np.abs(correction_complex - (paired_complex - (
            2.0 * paired_complex - high_complex
        ))))
    )
    direct_identity_residual = float(
        np.max(np.abs(correction_complex - (high_complex - paired_complex)))
    )
    arrays_finite = all(
        finite_array(value)
        for value in (
            high,
            paired,
            correction,
            independent,
            estimator,
            estimator_covariance,
            normalized_components,
        )
    )
    safe_se = np.where(estimator_se > 0.0, estimator_se, math.inf)
    jackknife_rows: list[dict[str, Any]] = []
    for index, seed in enumerate(high_seeds):
        candidate = (
            np.mean(np.delete(correction, index, axis=0), axis=0)
            + beta * np.mean(independent, axis=0)
        )
        shift = np.abs(candidate - estimator) / safe_se
        jackknife_rows.append(
            {
                "deletion_role": "high",
                "deleted_seed": seed,
                "maximum_shift_in_full_standard_errors": float(np.max(shift)),
                "worst_channel": labels[int(np.argmax(shift))],
            }
        )
    for index, seed in enumerate(low_seeds):
        candidate = (
            np.mean(correction, axis=0)
            + beta * np.mean(np.delete(independent, index, axis=0), axis=0)
        )
        shift = np.abs(candidate - estimator) / safe_se
        jackknife_rows.append(
            {
                "deletion_role": "low",
                "deleted_seed": seed,
                "maximum_shift_in_full_standard_errors": float(np.max(shift)),
                "worst_channel": labels[int(np.argmax(shift))],
            }
        )
    channel_rows = [
        {
            "channel": labels[index],
            "fixed_beta": beta,
            "estimate": float(estimator[index]),
            "standard_error": float(estimator_se[index]),
            "high_only_estimate": float(high_estimator[index]),
            "high_only_standard_error": float(high_se[index]),
            "same_high_sample_standard_error_ratio": float(
                estimator_se[index] / high_se[index]
            )
            if high_se[index] > 0.0
            else math.inf,
            "target_margin": float(margins[index]),
            "standard_error_over_margin": float(estimator_se[index] / margins[index]),
            "realized_cost_normalized_component_score_ratio": float(
                normalized_components[index]
            ),
            "is_bottleneck": index == worst_index,
        }
        for index in range(len(labels))
    ]
    write_csv(CHANNEL_CSV, channel_rows)
    write_csv(EVENT_CSV, event_rows)
    write_csv(JACKKNIFE_CSV, jackknife_rows)
    score_gate_passed = score_ratio < threshold
    runtime_gate_passed = accepted_runtime_hours <= runtime_cap_hours
    locked_gate_passed = score_gate_passed and runtime_gate_passed
    formal_digest = tree_digest(FORMAL)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "design_lock": str(DESIGN_LOCK),
        "design_lock_sha256": digest(DESIGN_LOCK),
        "design_result": str(DESIGN_RESULT),
        "design_result_sha256": digest(DESIGN_RESULT),
        "high_completion": str(HIGH_RUN / "COMPLETED.json"),
        "high_completion_sha256": digest(HIGH_RUN / "COMPLETED.json"),
        "control_completion": str(LOW_RUN / "COMPLETED.json"),
        "control_completion_sha256": digest(LOW_RUN / "COMPLETED.json"),
        "high_units": high_units,
        "low_units": low_units,
        "high_seeds": high_seeds,
        "low_seeds": low_seeds,
        "channel_order": labels,
        "fixed_beta_real": beta,
        "fixed_beta_imaginary": beta,
        "low_to_high_ratio": ratio,
        "fresh_control_data_used_to_fit_beta": False,
        "target_central_values_used": False,
        "paired_identity_residual": paired_identity_residual,
        "direct_identity_residual": direct_identity_residual,
        "estimator": estimator.tolist(),
        "estimator_standard_error": estimator_se.tolist(),
        "high_only_estimator": high_estimator.tolist(),
        "high_only_standard_error": high_se.tolist(),
        "high_samples": high.tolist(),
        "paired_control_samples": paired.tolist(),
        "correction_samples": correction.tolist(),
        "independent_control_samples": independent.tolist(),
        "correction_covariance": correction_covariance.tolist(),
        "control_covariance": control_covariance.tolist(),
        "estimator_covariance": estimator_covariance.tolist(),
        "mean_high_runtime_seconds": high_cost,
        "mean_control_runtime_seconds": control_cost,
        "accepted_final_job_runtime_seconds": accepted_runtime_seconds,
        "accepted_final_job_runtime_hours": accepted_runtime_hours,
        "runtime_accounting_scope": (
            "sum of accepted final high and control job records, matching the "
            "predeclared cost metric; failed exploratory/replay wall time is reported separately by checkpoints"
        ),
        "high_only_base_score": high_only_base_score,
        "realized_cost_normalized_component_score_ratios": normalized_components.tolist(),
        "realized_cost_normalized_score_ratio": score_ratio,
        "worst_channel": labels[worst_index],
        "predeclared_efficiency_threshold": threshold,
        "runtime_cap_hours": runtime_cap_hours,
        "score_gate_passed": score_gate_passed,
        "runtime_gate_passed": runtime_gate_passed,
        "locked_numerical_efficiency_gate_passed": locked_gate_passed,
        "decision": (
            "LOCKED_BETA_ONE_COMPLEX_CONTROL_PASSES"
            if locked_gate_passed
            else "LOCKED_BETA_ONE_COMPLEX_CONTROL_DOES_NOT_PASS"
        ),
        "maximum_estimator_standard_error_over_margin": float(
            np.max(estimator_se / margins)
        ),
        "maximum_high_only_standard_error_over_margin": float(
            np.max(high_se / margins)
        ),
        "maximum_delete_one_shift_in_full_standard_errors": max(
            row["maximum_shift_in_full_standard_errors"] for row in jackknife_rows
        ),
        "all_arrays_finite": arrays_finite,
        "design_conditioned": True,
        "independent_efficiency_claim_allowed": False,
        "result_scope": "design-conditioned numerical estimator efficiency only",
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, str(len(required))),
        ("design_hash_chain", digest(DESIGN_RESULT) == lock["source_result_sha256"], digest(DESIGN_RESULT)),
        ("high_matrix_complete", high_completion["completed_converged"] == 360, str(high_completion["completed_converged"])),
        ("control_matrix_complete", low_completion["completed_converged"] == 180, str(low_completion["completed_converged"])),
        ("config_digest_locked", high_config["config_digest"] == low_config["config_digest"] == lock["pilot_config_digest"], str(lock["pilot_config_digest"])),
        ("sample_allocation_locked", high_units == 4 and low_units == 12 and ratio == 3.0, f"{high_units}:{low_units}"),
        ("seed_sets_disjoint", not set(high_seeds).intersection(low_seeds), str(sorted(set(high_seeds).intersection(low_seeds)))),
        ("complex_beta_fixed", beta == 1.0 and float(lock["fixed_beta_imaginary"]) == 1.0, str(beta)),
        ("paired_identity_exact", max(paired_identity_residual, direct_identity_residual) < 1.0e-12, str(max(paired_identity_residual, direct_identity_residual))),
        ("all_arrays_finite", arrays_finite, str(arrays_finite)),
        ("no_fresh_fit_or_target_center", not result["fresh_control_data_used_to_fit_beta"] and not result["target_central_values_used"], "beta and margins fixed before controls"),
        ("score_decision_consistent", score_gate_passed == (score_ratio < threshold), f"{score_ratio} < {threshold}"),
        ("runtime_decision_consistent", runtime_gate_passed == (accepted_runtime_hours <= runtime_cap_hours), f"{accepted_runtime_hours} <= {runtime_cap_hours}"),
        ("joint_decision_consistent", locked_gate_passed == (score_gate_passed and runtime_gate_passed), result["decision"]),
        ("independent_claim_blocked", not result["independent_efficiency_claim_allowed"], "high data selected the route"),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], result["result_scope"]),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for name, passed, detail in checks:
            writer.writerow(
                {
                    "check": name,
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5120 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
