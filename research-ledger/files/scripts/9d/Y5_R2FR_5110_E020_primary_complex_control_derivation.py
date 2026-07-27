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
MANIFEST = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5076"
    / "locked_central_anchor_pilot_manifest.json"
)
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v12"
)
CONFIG = RUN / "config.json"
STATUS = RUN / "status.json"
ANALYSIS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5080"
    / "fresh_pilot_analysis_v12.json"
)
CHANNELS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5080"
    / "fresh_pilot_channels_v12.csv"
)
REFLECTION_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5109"
    / "upper_sheet_reflection_zero_control_gate.json"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5110"
RESULT_JSON = SOURCE / "E020_primary_complex_control_feasibility.json"
LOCK_JSON = SOURCE / "E020_primary_complex_control_design_lock.json"
CHANNEL_CSV = SOURCE / "E020_primary_complex_control_channels.csv"
ALLOCATION_CSV = SOURCE / "E020_primary_complex_control_allocation_sensitivity.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5110_VALIDATION.csv"
)
MARKER = "MTS_5110_E020_PRIMARY_COMPLEX_CONTROL_DERIVATION"
REVISION = "algebraic-complex-telescoping-beta1-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
FIXED_BETA = 1.0
FIXED_LOW_TO_HIGH_RATIO = 3.0
EFFICIENCY_THRESHOLD = 0.8
RUNTIME_CAP_HOURS = 10.0


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5080 = load_module("mts_5080_for_5110", SCRIPT_5080)


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


def component_variance(values: np.ndarray) -> np.ndarray:
    return np.var(values, axis=0, ddof=1)


def main() -> None:
    required = [
        SCRIPT_5080,
        MANIFEST,
        CONFIG,
        STATUS,
        ANALYSIS,
        CHANNELS,
        REFLECTION_GATE,
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    manifest = read_json(MANIFEST)
    config = read_json(CONFIG)
    status = read_json(STATUS)
    analysis = read_json(ANALYSIS)
    reflection = read_json(REFLECTION_GATE)
    old_channel_rows = read_csv(CHANNELS)
    base_ids = [str(row["argument_id"]) for row in config["base_arguments"]]
    lookup = M5080.M5077.M5036.event_lookup(config)
    seed_to_event = {
        int(row["seed"]): str(row["event_id"]) for row in lookup.values()
    }
    high_seeds = [int(value) for value in manifest["fresh_high_scramble_seeds"]]
    low_seeds = [int(value) for value in manifest["fresh_low_scramble_seeds"]]
    if len(high_seeds) != 4 or len(low_seeds) != 12:
        raise RuntimeError("5110 requires the locked four-high/twelve-low design")

    epsilon_020_values: list[np.ndarray] = []
    epsilon_040_values: list[np.ndarray] = []
    epsilon_020_costs: list[float] = []
    for seed in high_seeds:
        event_id = seed_to_event[seed]
        epsilon_020 = M5080.event_arguments(
            RUN, event_id, "E020", "primary24", base_ids
        )
        epsilon_040 = M5080.event_arguments(
            RUN, event_id, "E040", "primary24", base_ids
        )
        epsilon_020_values.append(
            M5080.M5077.M5043.cyclic_nonlocal(config, epsilon_020)
        )
        epsilon_040_values.append(
            M5080.M5077.M5043.cyclic_nonlocal(config, epsilon_040)
        )
        epsilon_020_costs.append(
            M5080.event_cost(
                RUN,
                event_id,
                [("E020", "primary24")],
                base_ids,
            )
        )

    epsilon_020_array = np.asarray(epsilon_020_values, dtype=np.complex128)
    epsilon_040_array = np.asarray(epsilon_040_values, dtype=np.complex128)
    high_array = 2.0 * epsilon_020_array - epsilon_040_array
    correction_array = high_array - epsilon_020_array
    identity_residual = float(
        np.max(
            np.abs(
                correction_array
                - (epsilon_020_array - epsilon_040_array)
            )
        )
    )
    high_components = component_matrix(high_array)
    control_components = component_matrix(epsilon_020_array)
    correction_components = component_matrix(correction_array)
    high_variance = component_variance(high_components)
    control_variance = component_variance(control_components)
    correction_variance = component_variance(correction_components)
    real_margins = np.asarray(
        [float(row["target_margin"]) for row in old_channel_rows[:5]],
        dtype=float,
    )
    margins = np.concatenate((real_margins, real_margins))
    labels = [
        *[f"real_z{float(value):+.1f}" for value in config["physical_cosines"]],
        *[f"imag_z{float(value):+.1f}" for value in config["physical_cosines"]],
    ]
    high_cost = float(analysis["mean_high_only_runtime_seconds"])
    control_cost = float(np.mean(epsilon_020_costs))
    high_only_base_score = float(
        np.max(np.sqrt(high_variance * high_cost) / margins)
    )

    def score(ratio: float, indices: np.ndarray | None = None) -> np.ndarray:
        if indices is None:
            local_high = high_components
            local_control = control_components
        else:
            local_high = high_components[indices]
            local_control = control_components[indices]
        local_high_variance = component_variance(local_high)
        local_control_variance = component_variance(local_control)
        local_correction_variance = component_variance(
            local_high - local_control
        )
        local_base = float(
            np.max(np.sqrt(local_high_variance * high_cost) / margins)
        )
        return (
            np.sqrt(
                (
                    local_correction_variance
                    + local_control_variance / ratio
                )
                * (high_cost + ratio * control_cost)
            )
            / margins
            / local_base
        )

    fixed_scores = score(FIXED_LOW_TO_HIGH_RATIO)
    fixed_global_score = float(np.max(fixed_scores))
    fixed_worst_channel = labels[int(np.argmax(fixed_scores))]
    leave_one_out_rows: list[dict[str, Any]] = []
    for deleted_index, deleted_seed in enumerate(high_seeds):
        kept = np.asarray(
            [index for index in range(len(high_seeds)) if index != deleted_index]
        )
        candidate = score(FIXED_LOW_TO_HIGH_RATIO, kept)
        leave_one_out_rows.append(
            {
                "deleted_seed": deleted_seed,
                "global_score": float(np.max(candidate)),
                "worst_channel": labels[int(np.argmax(candidate))],
            }
        )
    maximum_leave_one_out_score = max(
        float(row["global_score"]) for row in leave_one_out_rows
    )

    allocation_rows: list[dict[str, Any]] = []
    robust_best: tuple[float, float, float, float] | None = None
    for ratio in np.geomspace(0.5, 6.0, 800):
        full_score = float(np.max(score(float(ratio))))
        leave_one_out_scores = []
        for deleted_index in range(len(high_seeds)):
            kept = np.asarray(
                [
                    index
                    for index in range(len(high_seeds))
                    if index != deleted_index
                ]
            )
            leave_one_out_scores.append(
                float(np.max(score(float(ratio), kept)))
            )
        robust_score = max([full_score, *leave_one_out_scores])
        runtime_hours = (
            len(high_seeds) * high_cost
            + ratio * len(high_seeds) * control_cost
        ) / 3600.0
        if robust_best is None or robust_score < robust_best[0]:
            robust_best = (
                robust_score,
                float(ratio),
                full_score,
                runtime_hours,
            )
        if any(abs(float(ratio) - value) < 0.01 for value in (2.0, 3.0, 4.0)):
            allocation_rows.append(
                {
                    "low_to_high_ratio": float(ratio),
                    "full_score": full_score,
                    "maximum_leave_one_out_score": max(leave_one_out_scores),
                    "robust_score": robust_score,
                    "projected_runtime_hours": runtime_hours,
                }
            )
    assert robust_best is not None
    for integer_ratio in (2.0, 3.0, 4.0):
        candidate = score(integer_ratio)
        candidate_loo = []
        for deleted_index in range(len(high_seeds)):
            kept = np.asarray(
                [
                    index
                    for index in range(len(high_seeds))
                    if index != deleted_index
                ]
            )
            candidate_loo.append(float(np.max(score(integer_ratio, kept))))
        allocation_rows.append(
            {
                "low_to_high_ratio": integer_ratio,
                "full_score": float(np.max(candidate)),
                "maximum_leave_one_out_score": max(candidate_loo),
                "robust_score": max(float(np.max(candidate)), *candidate_loo),
                "projected_runtime_hours": (
                    len(high_seeds) * high_cost
                    + integer_ratio * len(high_seeds) * control_cost
                )
                / 3600.0,
            }
        )
    unique_allocations = {
        round(float(row["low_to_high_ratio"]), 9): row
        for row in allocation_rows
    }
    allocation_rows = [
        unique_allocations[key] for key in sorted(unique_allocations)
    ]

    projected_total_runtime_hours = (
        len(high_seeds) * high_cost + len(low_seeds) * control_cost
    ) / 3600.0
    projected_incremental_runtime_hours = (
        len(low_seeds) * control_cost / 3600.0
    )
    robust_ratio_four_runtime_hours = (
        len(high_seeds) * high_cost + 4.0 * len(high_seeds) * control_cost
    ) / 3600.0
    maximum_control_cost_for_ratio_four_under_cap = (
        RUNTIME_CAP_HOURS * 3600.0 - len(high_seeds) * high_cost
    ) / (4.0 * len(high_seeds))
    required_ratio_four_cost_reduction = (
        1.0 - maximum_control_cost_for_ratio_four_under_cap / control_cost
    )
    channel_rows = [
        {
            "channel": label,
            "fixed_beta": FIXED_BETA,
            "high_variance": float(high_variance[index]),
            "correction_variance": float(correction_variance[index]),
            "control_variance_design_proxy": float(control_variance[index]),
            "target_margin": float(margins[index]),
            "ratio3_cost_normalized_score": float(fixed_scores[index]),
            "is_ratio3_bottleneck": index == int(np.argmax(fixed_scores)),
        }
        for index, label in enumerate(labels)
    ]
    write_csv(CHANNEL_CSV, channel_rows)
    write_csv(ALLOCATION_CSV, allocation_rows)

    formal_digest = tree_digest(FORMAL)
    locked_matrix_complete = (
        int(status["completed_converged"]) == 360
        and bool(status["pilot_numerical_matrix_complete"])
    )
    ratio_three_design_feasible = (
        fixed_global_score < EFFICIENCY_THRESHOLD
        and projected_total_runtime_hours <= RUNTIME_CAP_HOURS
    )
    independent_efficiency_claim_allowed = False
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "verdict": "E020_PRIMARY_COMPLEX_CONTROL_PROMISING_BUT_DESIGN_CONDITIONED",
        "reflection_zero_control_rejected": reflection["verdict"]
        == "REFLECTION_ZERO_CONTROL_REJECTED_FOR_LOCKED_UPPER_SHEET",
        "exact_estimator_identity": {
            "high": "H=2 A_020-B_040",
            "control": "C=A_020",
            "fixed_beta": FIXED_BETA,
            "correction": "H-C=A_020-B_040",
            "expectation": "E[H-C]+E[C]=E[H] componentwise over C",
            "numerical_identity_residual": identity_residual,
            "requires_zero_imaginary_mean": False,
            "requires_reflection_symmetry": False,
        },
        "design_data": {
            "high_seeds": high_seeds,
            "candidate_low_seeds": low_seeds,
            "high_units": len(high_seeds),
            "candidate_low_units": len(low_seeds),
            "fresh_v12_high_data_used_to_choose_route": True,
            "independent_efficiency_claim_allowed": independent_efficiency_claim_allowed,
        },
        "measured_costs": {
            "mean_high_H_seconds": high_cost,
            "mean_E020_primary_control_seconds": control_cost,
            "projected_incremental_twelve_control_hours": projected_incremental_runtime_hours,
        },
        "fixed_ratio_three_design": {
            "low_to_high_ratio": FIXED_LOW_TO_HIGH_RATIO,
            "global_score": fixed_global_score,
            "worst_channel": fixed_worst_channel,
            "threshold": EFFICIENCY_THRESHOLD,
            "projected_total_runtime_hours": projected_total_runtime_hours,
            "runtime_cap_hours": RUNTIME_CAP_HOURS,
            "maximum_leave_one_high_out_score": maximum_leave_one_out_score,
            "leave_one_high_out": leave_one_out_rows,
            "design_feasible": ratio_three_design_feasible,
            "robust_pass_claimed": False,
        },
        "robust_allocation_diagnostic": {
            "best_maximum_full_and_leave_one_out_score": robust_best[0],
            "continuous_low_to_high_ratio": robust_best[1],
            "full_score_at_best_ratio": robust_best[2],
            "projected_runtime_hours_at_best_ratio": robust_best[3],
            "integer_ratio_four_runtime_hours": robust_ratio_four_runtime_hours,
            "maximum_control_cost_seconds_for_ratio_four_under_ten_hours": maximum_control_cost_for_ratio_four_under_cap,
            "required_control_cost_reduction_fraction": required_ratio_four_cost_reduction,
        },
        "decision": (
            "The algebraic beta=1 complex control is the first replacement route "
            "that clears 0.8 in the full design estimate while remaining under "
            "ten projected hours. It is borderline under leave-one-high-out and "
            "was selected using the v12 high data, so it authorizes a restartable "
            "design-conditioned extension, not an independent efficiency claim."
        ),
        "next_target": (
            "build a restartable E020-primary control-only runner for the twelve "
            "locked low events, capped at four hours per invocation; dry-run and "
            "predeclare beta=1, ratio=3, score<0.8, convergence, and runtime gates "
            "before executing any new kernel"
        ),
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    lock = {
        "checkpoint_marker": "MTS_5110_E020_PRIMARY_COMPLEX_CONTROL_DESIGN_LOCK",
        "revision": REVISION,
        "source_result": str(RESULT_JSON),
        "source_result_sha256": digest(RESULT_JSON),
        "pilot_config_digest": config["config_digest"],
        "high_observable": "H=2*R_primary(E020)-R_primary(E040)",
        "paired_control": "C=R_primary(E020)",
        "independent_control": "C=R_primary(E020)",
        "fixed_beta_real": FIXED_BETA,
        "fixed_beta_imaginary": FIXED_BETA,
        "high_seeds": high_seeds,
        "low_seeds": low_seeds,
        "low_to_high_ratio": FIXED_LOW_TO_HIGH_RATIO,
        "primary_decision_threshold": EFFICIENCY_THRESHOLD,
        "runtime_cap_hours": RUNTIME_CAP_HOURS,
        "incremental_invocation_wall_cap_hours": 4.0,
        "runner_implementation_authorized": True,
        "numerical_execution_authorized": False,
        "reason_execution_not_yet_authorized": "restartable runner and dry-run gate do not yet exist",
        "design_conditioned": True,
        "independent_efficiency_claim_allowed": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(LOCK_JSON, lock)

    checks = [
        ("sources_exist", not missing, "all 5110 sources exist"),
        ("locked_matrix_complete", locked_matrix_complete, "360/360 converged"),
        (
            "reflection_route_closed",
            result["reflection_zero_control_rejected"],
            reflection["verdict"],
        ),
        ("telescoping_identity_exact", identity_residual < 1.0e-12, str(identity_residual)),
        ("complex_beta_fixed", FIXED_BETA == 1.0, "beta_real=beta_imag=1"),
        (
            "ratio_three_score_below_threshold",
            fixed_global_score < EFFICIENCY_THRESHOLD,
            f"{fixed_global_score} < {EFFICIENCY_THRESHOLD}",
        ),
        (
            "ratio_three_runtime_within_cap",
            projected_total_runtime_hours <= RUNTIME_CAP_HOURS,
            f"{projected_total_runtime_hours} <= {RUNTIME_CAP_HOURS}",
        ),
        (
            "leave_one_out_borderline_recorded",
            maximum_leave_one_out_score >= EFFICIENCY_THRESHOLD,
            str(maximum_leave_one_out_score),
        ),
        (
            "execution_not_prematurely_authorized",
            not lock["numerical_execution_authorized"],
            lock["reason_execution_not_yet_authorized"],
        ),
        (
            "independent_claim_blocked",
            not independent_efficiency_claim_allowed,
            "v12 high data selected the route",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "estimator design only; no MTS physics claim",
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
                    "check_id": f"V5110_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5110 validation failed: {failed}")


if __name__ == "__main__":
    main()
