from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
ANALYSIS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5120"
    / "locked_beta_one_complex_control_analysis.json"
)
DESIGN_CHANNELS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5110"
    / "E020_primary_complex_control_channels.csv"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5121"
RESULT_JSON = SOURCE / "locked_beta_one_failure_mechanism.json"
CHANNEL_CSV = SOURCE / "control_variance_inflation_by_channel.csv"
ALLOCATION_CSV = SOURCE / "postdecision_allocation_diagnostic.csv"
DELETE_ONE_CSV = SOURCE / "delete_one_low_score_diagnostic.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5121_VALIDATION.csv"
)
MARKER = "MTS_5121_LOCKED_BETA_ONE_FAILURE_MECHANISM"
REVISION = "observed-control-variance-not-single-row-failure-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


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


def variance(values: np.ndarray) -> np.ndarray:
    return np.var(values, axis=0, ddof=1)


def main() -> None:
    required = [ANALYSIS, DESIGN_CHANNELS, FORMAL]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5121 inputs: {missing}")
    analysis = read_json(ANALYSIS)
    design_rows = read_csv(DESIGN_CHANNELS)
    labels = [str(row["channel"]) for row in design_rows]
    margins = np.asarray([float(row["target_margin"]) for row in design_rows])
    design_control_variance = np.asarray(
        [float(row["control_variance_design_proxy"]) for row in design_rows]
    )
    design_scores = np.asarray(
        [float(row["ratio3_cost_normalized_score"]) for row in design_rows]
    )
    high = np.asarray(analysis["high_samples"], dtype=float)
    correction = np.asarray(analysis["correction_samples"], dtype=float)
    control = np.asarray(analysis["independent_control_samples"], dtype=float)
    high_variance = variance(high)
    correction_variance = variance(correction)
    control_variance = variance(control)
    high_cost = float(analysis["mean_high_runtime_seconds"])
    control_cost = float(analysis["mean_control_runtime_seconds"])
    threshold = float(analysis["predeclared_efficiency_threshold"])
    runtime_cap = float(analysis["runtime_cap_hours"])
    high_units = int(analysis["high_units"])
    high_base = float(np.max(np.sqrt(high_variance * high_cost) / margins))

    def score(ratio: float, local_control: np.ndarray = control) -> np.ndarray:
        local_variance = variance(local_control)
        variance_cost = (
            correction_variance + local_variance / ratio
        ) * (high_cost + ratio * control_cost)
        return np.sqrt(np.maximum(variance_cost, 0.0)) / margins / high_base

    fixed_components = score(3.0)
    fixed_score = float(np.max(fixed_components))
    fixed_worst = labels[int(np.argmax(fixed_components))]
    maximum_ratio_under_cap = (
        runtime_cap * 3600.0 - high_units * high_cost
    ) / (high_units * control_cost)
    budget_ratios = np.linspace(0.25, maximum_ratio_under_cap, 2000)
    budget_rows = [
        {
            "low_to_high_ratio": float(ratio),
            "global_score": float(np.max(score(float(ratio)))),
            "worst_channel": labels[int(np.argmax(score(float(ratio))))],
            "projected_runtime_hours": float(
                high_units * (high_cost + float(ratio) * control_cost) / 3600.0
            ),
            "within_original_runtime_cap": True,
        }
        for ratio in budget_ratios
    ]
    unconstrained_ratios = np.linspace(0.25, 20.0, 4000)
    unconstrained_rows = [
        {
            "low_to_high_ratio": float(ratio),
            "global_score": float(np.max(score(float(ratio)))),
            "worst_channel": labels[int(np.argmax(score(float(ratio))))],
            "projected_runtime_hours": float(
                high_units * (high_cost + float(ratio) * control_cost) / 3600.0
            ),
            "within_original_runtime_cap": bool(
                high_units * (high_cost + float(ratio) * control_cost) / 3600.0
                <= runtime_cap
            ),
        }
        for ratio in unconstrained_ratios
    ]
    best_budget = min(budget_rows, key=lambda row: row["global_score"])
    best_unconstrained = min(
        unconstrained_rows, key=lambda row: row["global_score"]
    )
    selected_ratios = sorted(
        {
            1.0,
            2.0,
            3.0,
            maximum_ratio_under_cap,
            float(best_budget["low_to_high_ratio"]),
            float(best_unconstrained["low_to_high_ratio"]),
            4.0,
            6.0,
            10.0,
            20.0,
        }
    )
    allocation_rows = []
    for ratio in selected_ratios:
        components = score(ratio)
        runtime = high_units * (high_cost + ratio * control_cost) / 3600.0
        allocation_rows.append(
            {
                "low_to_high_ratio": ratio,
                "global_score": float(np.max(components)),
                "worst_channel": labels[int(np.argmax(components))],
                "projected_runtime_hours": runtime,
                "within_original_runtime_cap": runtime <= runtime_cap,
                "postdecision_diagnostic_only": True,
            }
        )
    delete_rows = []
    low_seeds = [int(value) for value in analysis["low_seeds"]]
    for index, seed in enumerate(low_seeds):
        local = np.delete(control, index, axis=0)
        local_ratio = local.shape[0] / high_units
        components = score(local_ratio, local)
        delete_rows.append(
            {
                "deleted_seed": seed,
                "remaining_low_units": local.shape[0],
                "realized_ratio": local_ratio,
                "global_score": float(np.max(components)),
                "worst_channel": labels[int(np.argmax(components))],
                "would_pass_original_score_gate": float(np.max(components))
                < threshold,
                "postdecision_diagnostic_only": True,
            }
        )
    channel_rows = []
    for index, label in enumerate(labels):
        inflation = control_variance[index] / max(
            design_control_variance[index], 1.0e-300
        )
        channel_rows.append(
            {
                "channel": label,
                "design_control_variance_proxy": float(
                    design_control_variance[index]
                ),
                "observed_independent_control_variance": float(
                    control_variance[index]
                ),
                "observed_over_design_variance_ratio": float(inflation),
                "correction_variance": float(correction_variance[index]),
                "control_variance_over_ratio_three": float(
                    control_variance[index] / 3.0
                ),
                "design_ratio3_score": float(design_scores[index]),
                "observed_ratio3_score": float(fixed_components[index]),
                "score_inflation_factor": float(
                    fixed_components[index] / max(design_scores[index], 1.0e-300)
                ),
                "is_observed_bottleneck": index == int(np.argmax(fixed_components)),
            }
        )
    write_csv(CHANNEL_CSV, channel_rows)
    write_csv(ALLOCATION_CSV, allocation_rows)
    write_csv(DELETE_ONE_CSV, delete_rows)
    worst_index = int(np.argmax(fixed_components))
    minimum_delete_score = min(row["global_score"] for row in delete_rows)
    formal_digest = tree_digest(FORMAL)
    mechanism_closed = bool(
        abs(fixed_score - float(analysis["realized_cost_normalized_score_ratio"]))
        < 1.0e-12
        and fixed_score >= threshold
        and float(best_budget["global_score"]) >= threshold
        and minimum_delete_score >= threshold
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "source_analysis": str(ANALYSIS),
        "source_analysis_sha256": digest(ANALYSIS),
        "locked_decision": analysis["decision"],
        "fixed_ratio_three_score_recomputed": fixed_score,
        "fixed_ratio_three_worst_channel": fixed_worst,
        "design_ratio_three_score": float(np.max(design_scores)),
        "score_increase_from_design": fixed_score - float(np.max(design_scores)),
        "worst_channel_observed_control_variance": float(
            control_variance[worst_index]
        ),
        "worst_channel_design_control_variance_proxy": float(
            design_control_variance[worst_index]
        ),
        "worst_channel_variance_inflation": float(
            control_variance[worst_index]
            / design_control_variance[worst_index]
        ),
        "worst_channel_correction_variance": float(
            correction_variance[worst_index]
        ),
        "worst_channel_control_variance_over_ratio_three": float(
            control_variance[worst_index] / 3.0
        ),
        "maximum_ratio_under_original_runtime_cap": float(
            maximum_ratio_under_cap
        ),
        "best_score_under_original_runtime_cap": best_budget,
        "best_unconstrained_score_through_ratio_twenty": best_unconstrained,
        "minimum_delete_one_low_score": float(minimum_delete_score),
        "any_delete_one_low_score_passes": any(
            row["would_pass_original_score_gate"] for row in delete_rows
        ),
        "failure_mechanism": (
            "Observed independent-control variance is materially larger and differently "
            "distributed across channels than the four-high design proxy. The failure "
            "survives every single-low deletion and every allocation permitted by the "
            "original ten-hour budget. It is not caused by runtime overrun or one bad row."
        ),
        "decision": (
            "LOCKED_BETA_ONE_CONTROL_VARIANCE_ROUTE_REJECTED_UNDER_ORIGINAL_BUDGET"
            if mechanism_closed
            else "FAILURE_MECHANISM_REQUIRES_MORE_AUDIT"
        ),
        "next_route": (
            "retain the completed high and control matrices as numerical evidence; do "
            "not retune beta or delete rows post hoc. Return to high-only hhh-cut/UV "
            "coefficient work unless a new control is derived and independently locked."
        ),
        "postdecision_diagnostics_change_locked_decision": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, str(len(required))),
        ("locked_failure_reproduced", abs(fixed_score - float(analysis["realized_cost_normalized_score_ratio"])) < 1.0e-12, str(fixed_score)),
        ("locked_score_still_fails", fixed_score >= threshold, f"{fixed_score} >= {threshold}"),
        ("runtime_budget_allocation_cannot_rescue", float(best_budget["global_score"]) >= threshold, str(best_budget)),
        ("no_single_low_deletion_rescues", minimum_delete_score >= threshold, str(minimum_delete_score)),
        ("diagnostics_do_not_change_decision", not result["postdecision_diagnostics_change_locked_decision"], result["locked_decision"]),
        ("mechanism_closed", mechanism_closed, result["failure_mechanism"]),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "estimator failure mechanism is not a physics claim"),
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
        raise RuntimeError(f"checkpoint 5121 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
